"""Regras de negócio do fluxo, moderação e exportação pública."""

from copy import deepcopy
from datetime import datetime, timezone

from .config import public_compliance, validate_config
from .models import PublicNameMode, Review, ReviewStatus, Sale, SaleStage

STAGE_ORDER = [stage.value for stage in SaleStage]


class CorrespondentService:
    def __init__(self, repository, config):
        validate_config(config)
        self.repository = repository
        self.config = config

    def create_sale(self, cliente_id, proposta_id):
        data = self.repository.load()
        sale = Sale(cliente_id=cliente_id, proposta_id=proposta_id)
        data["vendas"].append(sale.to_dict())
        self.repository.save(data)
        return sale.to_dict()

    def advance_sale(self, venda_id, etapa):
        if etapa not in STAGE_ORDER:
            raise ValueError("Etapa inválida.")
        data = self.repository.load()
        sale = self._find(data["vendas"], venda_id, "Venda")
        current = STAGE_ORDER.index(sale["etapa"])
        target = STAGE_ORDER.index(etapa)
        if target < current or target > current + 1:
            raise ValueError("A etapa deve avançar uma posição por vez.")
        sale["etapa"] = etapa
        sale["updated_at"] = self._now()
        self.repository.save(data)
        return deepcopy(sale)

    def request_review(self, venda_id):
        data = self.repository.load()
        sale = self._find(data["vendas"], venda_id, "Venda")
        if sale["etapa"] not in (SaleStage.VENDA_CONCLUIDA.value, SaleStage.POS_VENDA.value):
            raise ValueError("A avaliação só pode ser solicitada após a venda concluída.")
        if sale.get("avaliacao_solicitada_em"):
            raise ValueError("A avaliação já foi solicitada para esta venda.")
        sale["etapa"] = SaleStage.AVALIACAO_SOLICITADA.value
        sale["avaliacao_solicitada_em"] = self._now()
        sale["updated_at"] = sale["avaliacao_solicitada_em"]
        self.repository.save(data)
        return deepcopy(sale)

    def submit_review(self, venda_id, cliente_nome, nota, comentario, autoriza_publicacao, nome_publico_modo, nome_publico_customizado=None):
        if not isinstance(nota, int) or not 1 <= nota <= 5:
            raise ValueError("A nota deve estar entre 1 e 5.")
        if not comentario or not comentario.strip():
            raise ValueError("O comentário é obrigatório.")
        if nome_publico_modo not in [mode.value for mode in PublicNameMode]:
            raise ValueError("Modo de nome público inválido.")
        data = self.repository.load()
        sale = self._find(data["vendas"], venda_id, "Venda")
        if sale["etapa"] != SaleStage.AVALIACAO_SOLICITADA.value:
            raise ValueError("Não existe solicitação ativa para esta venda.")
        if any(item["venda_id"] == venda_id for item in data["avaliacoes"]):
            raise ValueError("Esta venda já possui avaliação.")
        review = Review(
            venda_id=venda_id,
            proposta_id=sale["proposta_id"],
            cliente_id=sale["cliente_id"],
            cliente_nome_interno=cliente_nome.strip(),
            nota=nota,
            comentario=comentario.strip(),
            autoriza_publicacao=bool(autoriza_publicacao),
            nome_publico_modo=nome_publico_modo,
            nome_publico_customizado=(nome_publico_customizado or "").strip() or None,
        )
        data["avaliacoes"].append(review.to_dict())
        self.repository.save(data)
        return review.to_dict()

    def moderate_review(self, avaliacao_id, status, comentario_moderado=None):
        if status not in (ReviewStatus.APROVADA.value, ReviewStatus.REJEITADA.value):
            raise ValueError("A moderação deve aprovar ou rejeitar.")
        data = self.repository.load()
        review = self._find(data["avaliacoes"], avaliacao_id, "Avaliação")
        if comentario_moderado is not None:
            review["comentario"] = comentario_moderado.strip()
        review["status"] = status
        review["publicada"] = False
        review["moderada_em"] = self._now()
        review["updated_at"] = review["moderada_em"]
        self.repository.save(data)
        return deepcopy(review)

    def set_review_visibility(self, avaliacao_id, publicada):
        data = self.repository.load()
        review = self._find(data["avaliacoes"], avaliacao_id, "Avaliação")
        if publicada and review["status"] != ReviewStatus.APROVADA.value:
            raise ValueError("Somente avaliações aprovadas podem ser publicadas.")
        if publicada and not review["autoriza_publicacao"]:
            raise ValueError("O cliente não autorizou a publicação.")
        review["publicada"] = bool(publicada)
        review["updated_at"] = self._now()
        self.repository.save(data)
        return deepcopy(review)

    def dashboard(self):
        data = self.repository.load()
        reviews = data["avaliacoes"]
        evaluated_sale_ids = {review["venda_id"] for review in reviews}
        requested = [sale for sale in data["vendas"] if sale.get("avaliacao_solicitada_em")]
        unanswered = [sale for sale in requested if sale["id"] not in evaluated_sale_ids]
        average = round(sum(r["nota"] for r in reviews) / len(reviews), 2) if reviews else 0
        counts = {status.value: sum(r["status"] == status.value for r in reviews) for status in ReviewStatus}
        return {
            "notaMedia": average,
            "quantidadeAvaliacoes": len(reviews),
            "porStatus": counts,
            "vendasComSolicitacao": [sale["id"] for sale in requested],
            "clientesPendentes": [sale["cliente_id"] for sale in unanswered],
        }

    def public_site_data(self):
        data = self.repository.load()
        public_reviews = []
        for review in data["avaliacoes"]:
            if not (review["status"] == ReviewStatus.APROVADA.value and review["publicada"] and review["autoriza_publicacao"]):
                continue
            public_reviews.append({
                "nota": review["nota"],
                "depoimento": review["comentario"],
                "nome": self._public_name(review),
                "data": review["created_at"][:10],
            })
        average = round(sum(item["nota"] for item in public_reviews) / len(public_reviews), 2) if public_reviews else 0
        return {
            "profissional": self.config["cliente"],
            "compliance": public_compliance(self.config),
            "avaliacoes": public_reviews,
            "resumoAvaliacoes": {"media": average, "quantidade": len(public_reviews)},
        }

    @staticmethod
    def _find(items, item_id, label):
        for item in items:
            if item["id"] == item_id:
                return item
        raise ValueError(f"{label} não encontrada.")

    @staticmethod
    def _public_name(review):
        if review.get("nome_publico_customizado"):
            return review["nome_publico_customizado"]
        name = review["cliente_nome_interno"].strip()
        mode = review["nome_publico_modo"]
        if mode == PublicNameMode.ANONIMO.value:
            return "Cliente verificado"
        parts = name.split()
        if mode == PublicNameMode.PRIMEIRO_NOME.value:
            return parts[0]
        if mode == PublicNameMode.INICIAIS.value:
            return ". ".join(part[0].upper() for part in parts) + "."
        return name

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()
