"""Testes das regras de compliance, pós-venda e privacidade."""

import json
import tempfile
import unittest
from pathlib import Path

from correspondent.config import public_compliance, validate_config
from correspondent.models import PublicNameMode, ReviewStatus, SaleStage
from correspondent.repository import JsonRepository
from correspondent.service import CorrespondentService


class CorrespondentServiceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.config = {
            "cliente": {"nome": "Karla Emanuelle", "whatsapp": "5581995217143"},
            "compliance": {
                "textoInstitucionalSeguro": "Atendimento profissional com informações claras.",
                "certificacoes": [], "credenciamentos": [], "instituicoesParceiras": [],
                "bancos": [], "informacoesRegulatorias": [], "dadosEmpresa": [], "dadosProfissionais": [],
            },
            "avaliacoes": {"exigirAutorizacaoPublicacao": True, "exigirAprovacaoManual": True},
        }
        self.service = CorrespondentService(JsonRepository(Path(self.temp.name) / "crm.json"), self.config)

    def tearDown(self):
        self.temp.cleanup()

    def _completed_sale(self):
        sale = self.service.create_sale("cliente-1", "proposta-1")
        for stage in [SaleStage.ATENDIMENTO, SaleStage.SIMULACAO, SaleStage.PROPOSTA, SaleStage.VENDA_CONCLUIDA]:
            sale = self.service.advance_sale(sale["id"], stage.value)
        return sale

    def test_review_requires_completed_sale(self):
        sale = self.service.create_sale("cliente-1", "proposta-1")
        with self.assertRaises(ValueError):
            self.service.request_review(sale["id"])

    def test_approved_review_is_not_public_without_consent_and_visibility(self):
        sale = self._completed_sale()
        self.service.request_review(sale["id"])
        review = self.service.submit_review(sale["id"], "Maria Silva", 5, "Atendimento claro.", False, PublicNameMode.PRIMEIRO_NOME.value)
        self.service.moderate_review(review["id"], ReviewStatus.APROVADA.value)
        self.assertEqual([], self.service.public_site_data()["avaliacoes"])
        with self.assertRaises(ValueError):
            self.service.set_review_visibility(review["id"], True)

    def test_public_export_excludes_internal_identifiers(self):
        sale = self._completed_sale()
        self.service.request_review(sale["id"])
        review = self.service.submit_review(sale["id"], "Maria Silva", 5, "Atendimento claro.", True, PublicNameMode.INICIAIS.value)
        self.service.moderate_review(review["id"], ReviewStatus.APROVADA.value)
        self.service.set_review_visibility(review["id"], True)
        item = self.service.public_site_data()["avaliacoes"][0]
        self.assertEqual("M. S.", item["nome"])
        self.assertNotIn("cliente_id", item)
        self.assertNotIn("venda_id", item)
        self.assertNotIn("proposta_id", item)

    def test_dashboard_tracks_pending_customers(self):
        sale = self._completed_sale()
        self.service.request_review(sale["id"])
        dashboard = self.service.dashboard()
        self.assertEqual(["cliente-1"], dashboard["clientesPendentes"])
        self.assertEqual(0, dashboard["quantidadeAvaliacoes"])

    def test_unconfirmed_compliance_item_cannot_be_published(self):
        config = json.loads(json.dumps(self.config))
        config["compliance"]["certificacoes"] = [{"texto": "Certificação X", "confirmado": False, "publicar": True}]
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_only_confirmed_compliance_is_exported(self):
        config = json.loads(json.dumps(self.config))
        config["compliance"]["bancos"] = [
            {"texto": "Instituição confirmada", "confirmado": True, "publicar": True},
            {"texto": "Rascunho interno", "confirmado": False, "publicar": False},
        ]
        self.assertEqual([{"texto": "Instituição confirmada"}], public_compliance(config)["bancos"])


if __name__ == "__main__":
    unittest.main()
