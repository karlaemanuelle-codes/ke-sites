import pytest

from commerce.config import default_commerce_config
from commerce.models import InstallmentInterestMode, PaymentFeeMode
from commerce.pricing import calculate_installment_table, calculate_pix_price, calculate_price


def test_pix_price_merchant_absorbs_equals_face_value():
    config = default_commerce_config()
    result = calculate_pix_price(amount=1000.0, config=config)
    assert result.customer_total == 1000.0
    assert result.gateway_fee_amount == pytest.approx(1000.0 * 0.0099, abs=0.01)
    assert result.net_to_ke_sites == pytest.approx(1000.0 - result.gateway_fee_amount, abs=0.01)


def test_credit_avista_customer_pays_mode_adds_fee_on_top():
    config = default_commerce_config()
    config["payment_fee_mode"] = PaymentFeeMode.CUSTOMER_PAYS
    result = calculate_price(amount=1000.0, method="CREDIT_AVISTA", installments=1, config=config)
    expected_fee = 1000.0 * 0.0399
    assert result.customer_total == pytest.approx(1000.0 + expected_fee, abs=0.01)
    assert result.net_to_ke_sites == 1000.0


def test_installment_value_times_n_equals_customer_total():
    config = default_commerce_config()
    amount = 3997.0
    for n in (1, 3, 6, 12):
        opt = calculate_price(amount=amount, method="CREDIT_PARCELADO" if n > 1 else "CREDIT_AVISTA", installments=n, config=config)
        assert opt.installment_value * n == pytest.approx(opt.customer_total, abs=0.05)


def test_sem_juros_label_never_lies():
    config = default_commerce_config()
    config["installment_interest_mode"] = InstallmentInterestMode.SEM_JUROS
    opt = calculate_price(amount=1000.0, method="CREDIT_PARCELADO", installments=6, config=config)
    assert "sem juros" in opt.label
    assert opt.has_interest is False


def test_juros_do_cliente_label_never_claims_sem_juros():
    config = default_commerce_config()
    config["installment_interest_mode"] = InstallmentInterestMode.JUROS_DO_CLIENTE
    config["customer_interest_percent"] = {n: 0.02 for n in range(1, 13)}
    opt = calculate_price(amount=1000.0, method="CREDIT_PARCELADO", installments=6, config=config)
    assert "sem juros" not in opt.label
    assert opt.has_interest is True
    assert opt.customer_total > 1000.0


def test_pix_not_installable():
    config = default_commerce_config()
    with pytest.raises(ValueError):
        calculate_price(amount=100.0, method="PIX", installments=2, config=config)


def test_installments_beyond_max_rejected():
    config = default_commerce_config()
    with pytest.raises(ValueError):
        calculate_price(amount=100.0, method="CREDIT_PARCELADO", installments=13, config=config)


def test_installment_table_stops_below_minimum_value():
    config = default_commerce_config()
    config["min_installment_value"] = 500.0
    options = calculate_installment_table(amount=1000.0, config=config)
    assert all(opt.installment_value >= 500.0 for opt in options)
    assert len(options) < 12


def test_hybrid_fee_split_between_customer_and_merchant():
    config = default_commerce_config()
    config["payment_fee_mode"] = PaymentFeeMode.HYBRID
    config["hybrid_fee_split_customer"] = 0.5
    result = calculate_price(amount=1000.0, method="CREDIT_AVISTA", installments=1, config=config)
    fee = 1000.0 * 0.0399
    assert result.customer_total == pytest.approx(1000.0 + fee * 0.5, abs=0.02)
    assert result.net_to_ke_sites == pytest.approx(1000.0 - fee * 0.5, abs=0.02)


def test_pix_discount_reduces_customer_total_and_net():
    config = default_commerce_config()
    config["pix_discount_percent"] = 0.05
    result = calculate_pix_price(amount=1000.0, config=config)
    assert result.customer_total < 1000.0
