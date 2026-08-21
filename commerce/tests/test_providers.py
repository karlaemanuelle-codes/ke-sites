import pytest

from commerce.models import Order, PaymentStatus
from commerce.providers import (
    ManualProvider,
    MercadoPagoProvider,
    NotConnectedError,
    StripeProvider,
    TonProvider,
    get_provider,
)


def make_order():
    return Order(
        id="ord-1", customer_id="c1", template_id="salao-de-beleza", plan_id="intermediario",
        market="BR", currency="BRL", subtotal=3997.0, total=3997.0,
    )


@pytest.mark.parametrize("provider_cls", [TonProvider, StripeProvider, MercadoPagoProvider])
def test_unconnected_providers_refuse_to_charge(provider_cls):
    provider = provider_cls()
    with pytest.raises(NotConnectedError):
        provider.create_charge(make_order())


@pytest.mark.parametrize("provider_cls", [TonProvider, StripeProvider, MercadoPagoProvider])
def test_unconnected_providers_refuse_webhooks(provider_cls):
    provider = provider_cls()
    with pytest.raises(NotConnectedError):
        provider.verify_webhook(b"{}", {})


def test_ton_supports_installments():
    assert TonProvider().supports_installments() is True


def test_stripe_supports_recurring():
    assert StripeProvider().supports_recurring() is True


def test_manual_provider_creates_pending_charge():
    provider = ManualProvider()
    result = provider.create_charge(make_order())
    assert result.status == PaymentStatus.PENDING
    assert result.provider == "manual"


def test_manual_provider_review_flow():
    provider = ManualProvider()
    order = make_order()
    status = provider.mark_reviewed(order, approved=True, reviewed_by="admin@kesites.com")
    assert status == PaymentStatus.APPROVED
    assert order.payment_status == PaymentStatus.APPROVED


def test_get_provider_registry():
    assert isinstance(get_provider("ton"), TonProvider)
    with pytest.raises(ValueError):
        get_provider("nao_existe")
