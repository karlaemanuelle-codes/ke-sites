import pytest

from commerce.config import default_commerce_config
from commerce.models import Promotion, PromotionType
from commerce.promotions import EligibilityContext, apply_promotion, check_margin, is_promotion_eligible


def make_promo(**overrides):
    base = dict(
        id="promo-1",
        name="Lançamento",
        description="Preço de lançamento",
        code=None,
        type=PromotionType.PERCENTAGE_DISCOUNT,
        value=0.10,
        currency="BRL",
        market="BR",
        start_date=None,
        end_date=None,
        usage_limit=None,
        per_customer_limit=None,
        active=True,
    )
    base.update(overrides)
    return Promotion(**base)


def test_inactive_promotion_never_eligible():
    promo = make_promo(active=False)
    ctx = EligibilityContext(template_id="salao-de-beleza", plan_id="intermediario", market="BR")
    assert is_promotion_eligible(promo, ctx) is False


def test_wrong_coupon_code_not_eligible():
    promo = make_promo(code="LANCAMENTO")
    ctx = EligibilityContext(template_id="x", plan_id="y", market="BR", coupon_code="OUTRO")
    assert is_promotion_eligible(promo, ctx) is False


def test_plan_restriction_respected():
    promo = make_promo(eligible_plans=["avancado"])
    ctx = EligibilityContext(template_id="x", plan_id="basico", market="BR")
    assert is_promotion_eligible(promo, ctx) is False


def test_market_restriction_respected():
    promo = make_promo(market="ES")
    ctx = EligibilityContext(template_id="x", plan_id="basico", market="BR")
    assert is_promotion_eligible(promo, ctx) is False


def test_apply_percentage_discount():
    promo = make_promo(type=PromotionType.PERCENTAGE_DISCOUNT, value=0.10)
    result = apply_promotion(amount=1000.0, promotion=promo)
    assert result == 900.0


def test_apply_fixed_discount_never_negative():
    promo = make_promo(type=PromotionType.FIXED_DISCOUNT, value=5000.0)
    result = apply_promotion(amount=1000.0, promotion=promo)
    assert result == 0.0


def test_bundle_type_not_a_simple_discount():
    promo = make_promo(type=PromotionType.BUNDLE, value=0.0)
    with pytest.raises(ValueError):
        apply_promotion(amount=1000.0, promotion=promo)


def test_margin_check_flags_below_minimum():
    config = default_commerce_config()
    config["minimum_margin_percentage"] = 0.35
    result = check_margin(
        gross_amount=1000.0,
        discount_amount=400.0,
        gateway_fee_amount=40.0,
        commission_amount=100.0,
        other_costs=0.0,
        config=config,
    )
    assert result.margin_percentage == pytest.approx(0.46, abs=0.01)
    assert result.requires_admin_approval is False


def test_margin_check_flags_when_too_low():
    config = default_commerce_config()
    config["minimum_margin_percentage"] = 0.60
    result = check_margin(
        gross_amount=1000.0,
        discount_amount=400.0,
        gateway_fee_amount=40.0,
        commission_amount=100.0,
        other_costs=0.0,
        config=config,
    )
    assert result.requires_admin_approval is True
