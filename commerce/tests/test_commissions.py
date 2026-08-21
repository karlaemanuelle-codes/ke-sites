import pytest

from commerce.commissions import (
    approve_commission,
    cancel_commission,
    create_commission_for_order,
    eligible_for_payout,
)
from commerce.config import default_commerce_config
from commerce.models import CommissionBase, CommissionStatus, Order, PaymentStatus


def make_order(**overrides):
    base = dict(
        id="ord-1",
        customer_id="cust-1",
        template_id="salao-de-beleza",
        plan_id="intermediario",
        market="BR",
        currency="BRL",
        subtotal=3997.0,
        discount=0.0,
        payment_fee=159.0,
        total=3997.0,
        affiliate_id="afiliado-1",
        payment_status=PaymentStatus.APPROVED,
    )
    base.update(overrides)
    return Order(**base)


def test_no_commission_without_affiliate():
    order = make_order(affiliate_id=None)
    config = default_commerce_config()
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    assert commission is None


def test_commission_requires_approved_payment():
    order = make_order(payment_status=PaymentStatus.PENDING)
    config = default_commerce_config()
    with pytest.raises(ValueError):
        create_commission_for_order(order=order, config=config, commission_id="c1")


def test_commission_gross_order_uses_subtotal_minus_discount():
    order = make_order(subtotal=3997.0, discount=200.0)
    config = default_commerce_config()
    config["commission_base"] = CommissionBase.GROSS_ORDER
    config["commission_rate"] = 0.10
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    assert commission.base_amount == pytest.approx(3797.0)
    assert commission.amount == pytest.approx(379.70)
    assert commission.status == CommissionStatus.PENDING


def test_commission_net_order_uses_total_minus_fee():
    order = make_order(total=3997.0, payment_fee=159.0)
    config = default_commerce_config()
    config["commission_base"] = CommissionBase.NET_ORDER
    config["commission_rate"] = 0.10
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    assert commission.base_amount == pytest.approx(3838.0)


def test_commission_custom_requires_configured_function():
    order = make_order()
    config = default_commerce_config()
    config["commission_base"] = CommissionBase.CUSTOM
    with pytest.raises(ValueError):
        create_commission_for_order(order=order, config=config, commission_id="c1")


def test_full_lifecycle_click_to_approved():
    order = make_order()
    config = default_commerce_config()
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    assert commission.status == CommissionStatus.PENDING
    approve_commission(commission)
    assert commission.status == CommissionStatus.APPROVED


def test_cancelled_order_cancels_commission_not_paid():
    order = make_order()
    config = default_commerce_config()
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    cancel_commission(commission)
    assert commission.status == CommissionStatus.CANCELLED


def test_paid_commission_cannot_be_cancelled():
    order = make_order()
    config = default_commerce_config()
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    commission.status = CommissionStatus.PAID
    with pytest.raises(ValueError):
        cancel_commission(commission)


def test_eligible_for_payout_requires_approved_and_min_value():
    order = make_order()
    config = default_commerce_config()
    config["commission_min_payout"] = 500.0
    commission = create_commission_for_order(order=order, config=config, commission_id="c1")
    approve_commission(commission)
    assert eligible_for_payout(commission, config=config) is False  # 399,70 < 500
    commission.amount = 600.0
    assert eligible_for_payout(commission, config=config) is True
