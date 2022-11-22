import json
import pytest
from django.urls import reverse

from .conftest import *


@pytest.mark.usefixtures("create_items")
@pytest.mark.django_db
def test_get_item(client):
    url = reverse("get_item", args=[pytest.item1.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["item"].name == pytest.item1.name


@pytest.mark.django_db
def test_get_item_not_found(client):
    url = reverse("get_item", args=[1])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.usefixtures("create_order")
@pytest.mark.django_db
def test_get_order(client):
    url = reverse("get_order", args=[pytest.order.id])
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response.context["order"]["discount"]["discount_value"]
        == pytest.discount.discount_value
    )
    assert len(response.context["order"]["items"]) == 1


@pytest.mark.django_db
def test_get_order_not_found(client):
    url = reverse("get_order", args=[1])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.usefixtures("create_items")
@pytest.mark.django_db
def test_handle_session_for_item(mocked_responses, client):
    json_data = {
        "id": "cs_test_a1zDuXbgRufiLkGWSg1io6jaKE0ZQCBjdJzS1MkISSoHnMUOgUEaCvQrEM",
    }
    mocked_responses.post(
        "https://api.stripe.com/v1/checkout/sessions",
        status=201,
        json=json_data,
    )
    url = reverse("create_session_item", args=[pytest.item1.id])
    response = client.post(url)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8").replace("'", '"'))["id"]
        == json_data["id"]
    )


@pytest.mark.django_db
def test_handle_session_for_item_404(client):
    url = reverse("create_session_item", args=[1])
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.usefixtures("create_order_items")
@pytest.mark.django_db
def test_handle_session_for_order(mocked_responses, client):
    json_data = {
        "id": "cs_test_a1zDuXbgRufiLkGWSg1io6jaKE0ZQCBjdJzS1MkISSoHnMUOgUEaCvQrEM",
    }
    mocked_responses.post(
        "https://api.stripe.com/v1/coupons",
        status=201,
        json={
            "id": "Z4OV52SU",
            "object": "coupon",
            "created": 1669112660,
            "currency": "usd",
            "duration": "repeating",
            "duration_in_months": 3,
            "percent_off": 25.5,
            "times_redeemed": 0,
            "valid": True,
        },
    )
    mocked_responses.post(
        "https://api.stripe.com/v1/tax_rates",
        status=201,
        json={
            "id": "txr_1M6tfgF2py4umjAfqWKdCIgk",
            "object": "tax_rate",
            "active": True,
            "country": "DE",
            "created": 1669112744,
            "description": "VAT Germany",
            "display_name": "VAT",
            "inclusive": False,
            "jurisdiction": "DE",
            "metadata": {},
            "percentage": 19.0,
            "tax_type": "vat",
        },
    )
    mocked_responses.post(
        "https://api.stripe.com/v1/checkout/sessions",
        status=201,
        json=json_data,
    )
    url = reverse("create_session_order", args=[pytest.order.id])
    response = client.post(url)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8").replace("'", '"'))["id"]
        == json_data["id"]
    )


@pytest.mark.django_db
def test_handle_session_for_order_404(client):
    url = reverse("create_session_order", args=[1])
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.usefixtures("create_items")
@pytest.mark.django_db
def test_handle_payment_for_item(mocked_responses, client):
    json_data = {
        "client_secret": "pi_3M6H5rF2py4umjAf0j4zfAJx_secret_QaZCYhHdFqeXujblBDlcSxEuh"
    }
    mocked_responses.post(
        "https://api.stripe.com/v1/payment_intents",
        status=201,
        json=json_data,
    )
    url = reverse("create_payment_intent_item", args=[pytest.item1.id])
    response = client.post(url)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8").replace("'", '"'))["client_secret"]
        == json_data["client_secret"]
    )


@pytest.mark.django_db
def test_handle_payment_for_item_404(client):
    url = reverse("create_payment_intent_item", args=[1])
    response = client.post(url)
    assert response.status_code == 404


@pytest.mark.usefixtures("create_order_items")
@pytest.mark.django_db
def test_handle_payment_for_order(mocked_responses, client):
    json_data = {
        "client_secret": "pi_3M6H5rF2py4umjAf0j4zfAJx_secret_QaZCYhHdFqeXujblBDlcSxEuh"
    }
    mocked_responses.post(
        "https://api.stripe.com/v1/payment_intents",
        status=201,
        json=json_data,
    )
    url = reverse("create_payment_order", args=[pytest.order.id])
    response = client.post(url)
    assert response.status_code == 200
    assert (
        json.loads(response.content.decode("utf-8").replace("'", '"'))["client_secret"]
        == json_data["client_secret"]
    )


@pytest.mark.django_db
def test_handle_payment_for_order_404(client):
    url = reverse("create_payment_order", args=[1])
    response = client.post(url)
    assert response.status_code == 404
