"""Entidades e estados do fluxo de pós-venda."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class SaleStage(str, Enum):
    LEAD = "LEAD"
    ATENDIMENTO = "ATENDIMENTO"
    SIMULACAO = "SIMULACAO"
    PROPOSTA = "PROPOSTA"
    VENDA_CONCLUIDA = "VENDA_CONCLUIDA"
    POS_VENDA = "POS_VENDA"
    AVALIACAO_SOLICITADA = "AVALIACAO_SOLICITADA"


class ReviewStatus(str, Enum):
    PENDENTE_APROVACAO = "PENDENTE_APROVACAO"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"


class PublicNameMode(str, Enum):
    NOME_COMPLETO = "nome_completo"
    PRIMEIRO_NOME = "primeiro_nome"
    INICIAIS = "iniciais"
    ANONIMO = "anonimo"


@dataclass
class Sale:
    cliente_id: str
    proposta_id: str
    id: str = field(default_factory=lambda: str(uuid4()))
    etapa: str = SaleStage.LEAD.value
    avaliacao_solicitada_em: Optional[str] = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self):
        return asdict(self)


@dataclass
class Review:
    venda_id: str
    proposta_id: str
    cliente_id: str
    cliente_nome_interno: str
    nota: int
    comentario: str
    autoriza_publicacao: bool
    nome_publico_modo: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: str = ReviewStatus.PENDENTE_APROVACAO.value
    nome_publico_customizado: Optional[str] = None
    publicada: bool = False
    moderada_em: Optional[str] = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self):
        return asdict(self)
