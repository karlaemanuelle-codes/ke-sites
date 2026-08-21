"""
providers.py — abstração de provedor de pagamento (seções 6, 7, 31 do adendo).

PaymentProvider define o contrato que qualquer gateway precisa cumprir para
o checkout da KE Sites funcionar sem reconstrução. Os adapters concretos
(TonProvider, StripeProvider, MercadoPagoProvider) são ESQUELETOS — eles
levantam NotConnectedError em qualquer operação que exigiria uma conta e
credenciais reais, porque nenhuma delas existe neste projeto.

REGRA TON (seção 31): antes de qualquer integração real, consulte a
documentação oficial vigente da Ton (https://www.ton.com.br ou o portal de
desenvolvedor do provedor escolhido) — as taxas variam por produto, volume,
plano, prazo, bandeira e condição promocional, e não devem ser copiadas de
uma fonte desatualizada. Nada neste arquivo assume uma taxa real.

ManualProvider é o único adapter "funcional": ele modela o fluxo de
pagamento manual (seção 23) — Pix/transferência conferidos manualmente por
um administrador — porque isso não depende de nenhuma conta de gateway.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from .models import Order, PaymentEvent, PaymentStatus


class NotConnectedError(RuntimeError):
    """Levantado quando uma operação exige uma conta/credencial real que
    este projeto não possui. Não é um bug — é o estado esperado até que um
    administrador configure a conta real do provedor (seção 40, itens 1-2)."""


@dataclass(frozen=True)
class ChargeResult:
    provider: str
    provider_reference: str
    status: PaymentStatus
    payment_link: Optional[str] = None
    pix_qr_code: Optional[str] = None
    pix_copy_paste: Optional[str] = None


class PaymentProvider(ABC):
    """Contrato que todo adapter de gateway deve implementar."""

    name: str

    @abstractmethod
    def create_charge(self, order: Order) -> ChargeResult:
        """Inicia uma cobrança (Pix, cartão à vista ou parcelado) para o
        pedido informado."""

    @abstractmethod
    def verify_webhook(self, raw_body: bytes, headers: dict) -> PaymentEvent:
        """Valida a autenticidade de um webhook recebido e o converte em um
        PaymentEvent. Deve rejeitar payloads não assinados/inválidos."""

    @abstractmethod
    def refund(self, order: Order, amount: Optional[float] = None) -> ChargeResult:
        """Solicita reembolso total (amount=None) ou parcial."""

    def supports_installments(self) -> bool:
        return False

    def supports_recurring(self) -> bool:
        return False


class _UnconnectedProviderBase(PaymentProvider):
    """Implementação comum aos adapters ainda não conectados a uma conta
    real — evita repetir o mesmo NotConnectedError em cada adapter."""

    def create_charge(self, order: Order) -> ChargeResult:
        raise NotConnectedError(
            f"{self.name}: nenhuma conta/credencial real configurada neste projeto. "
            f"Configure a conta real e as credenciais (seção 40, itens 1-2) antes de "
            f"chamar create_charge()."
        )

    def verify_webhook(self, raw_body: bytes, headers: dict) -> PaymentEvent:
        raise NotConnectedError(
            f"{self.name}: não há servidor real recebendo webhooks deste provedor "
            f"neste projeto (site estático, sem backend exposto)."
        )

    def refund(self, order: Order, amount: Optional[float] = None) -> ChargeResult:
        raise NotConnectedError(f"{self.name}: nenhuma conta real configurada.")


class TonProvider(_UnconnectedProviderBase):
    """Provedor preferencial para o Brasil (seção 7). Pix, cartão e
    parcelamento em até 12x via Link de Pagamento, segundo a documentação
    oficial da Ton — a ser confirmada antes de qualquer integração real."""
    name = "ton"

    def supports_installments(self) -> bool:
        return True


class StripeProvider(_UnconnectedProviderBase):
    """Alternativa internacional (EUA/Espanha) — cartão, Apple Pay, Google
    Pay, conforme disponibilidade por mercado (seção 19)."""
    name = "stripe"

    def supports_recurring(self) -> bool:
        return True


class MercadoPagoProvider(_UnconnectedProviderBase):
    """Alternativa para o Brasil (seção 7) — fallback futuro."""
    name = "mercado_pago"

    def supports_installments(self) -> bool:
        return True


class FutureProvider(_UnconnectedProviderBase):
    """Placeholder para um provedor ainda não decidido — existe só para
    provar que o checkout não fica preso a um único gateway (seção 6)."""
    name = "future_provider"


class ManualProvider(PaymentProvider):
    """Pagamento manual (seção 23) — Pix/transferência conferidos por um
    administrador. É o único adapter que não depende de uma conta de
    gateway, então é o único que realmente "funciona" neste projeto."""
    name = "manual"

    def create_charge(self, order: Order) -> ChargeResult:
        return ChargeResult(
            provider=self.name,
            provider_reference=f"manual-{order.id}",
            status=PaymentStatus.PENDING,
        )

    def verify_webhook(self, raw_body: bytes, headers: dict) -> PaymentEvent:
        raise NotConnectedError("manual: não há webhook — aprovação é manual, pelo admin.")

    def refund(self, order: Order, amount: Optional[float] = None) -> ChargeResult:
        return ChargeResult(
            provider=self.name,
            provider_reference=f"manual-refund-{order.id}",
            status=PaymentStatus.REFUNDED,
        )

    def mark_reviewed(self, order: Order, approved: bool, reviewed_by: str) -> PaymentStatus:
        """Fluxo real do pagamento manual: um administrador confere o
        comprovante e marca aprovado/cancelado (seção 23)."""
        order.payment_status = PaymentStatus.APPROVED if approved else PaymentStatus.CANCELLED
        return order.payment_status


PROVIDER_REGISTRY: dict[str, type[PaymentProvider]] = {
    "ton": TonProvider,
    "stripe": StripeProvider,
    "mercado_pago": MercadoPagoProvider,
    "future_provider": FutureProvider,
    "manual": ManualProvider,
}


def get_provider(name: str) -> PaymentProvider:
    try:
        return PROVIDER_REGISTRY[name]()
    except KeyError as exc:
        raise ValueError(f"Provedor desconhecido: {name}") from exc
