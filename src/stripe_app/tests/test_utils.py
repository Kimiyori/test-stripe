import pytest

from stripe_app.utils.app_utils import convert_to_stripe_currency


def test_convert_currency():
    res = convert_to_stripe_currency(121)
    assert res == 12100


def test_convert_currency_str():
    res = convert_to_stripe_currency("121")
    assert res == 12100


def test_convert_currency_str_fail():
    with pytest.raises(ValueError):
        convert_to_stripe_currency("eeee")
