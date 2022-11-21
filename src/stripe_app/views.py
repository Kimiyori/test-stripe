from typing import Any

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse

from rest_framework.views import APIView

from stripe_app.models import Item
from stripe_app.services.db_services import get_item, get_order
from stripe_app.services.stripe_services import (
    create_payment_for_item,
    create_payment_for_order,
    create_session_for_item,
    create_session_for_order,
)


class SuccesView(TemplateView):
    """View for success payment"""

    template_name: str = "success.html"


class FailView(TemplateView):
    """View if something during payemnt went wrong"""

    template_name: str = "fail.html"


class ItemView(TemplateView):
    """Item View"""

    template_name = "stripe_app/item.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(dict(item=get_object_or_404(Item, pk=kwargs.get("pk"))))
        return context


class OrderView(TemplateView):
    """View order"""

    template_name = "stripe_app/order.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        order_id = kwargs.get("order_pk")
        assert isinstance(order_id, int)
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(
            get_order(
                order_pk=order_id,
                fields=("items", "discount", "tax", "unit_amount"),
            )
        )
        context.update({"order": order})
        return context


class StripeSessionItemView(APIView):
    """View for handle iem payment with stripe session"""

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        item_id = kwargs.get("pk")
        assert isinstance(item_id, int)
        item = get_object_or_404(get_item(item_pk=item_id))
        session = create_session_for_item(request, item)  # type:ignore
        return JsonResponse({"id": session.id})


class StripeIntentItemView(APIView):
    """View for handle payment for item"""

    def post(
        self, request: HttpRequest, **kwargs: Any  # pylint: disable=unused-argument
    ) -> HttpResponse:
        item_id = kwargs.get("pk")
        assert isinstance(item_id, int)
        item = get_object_or_404(get_item(item_pk=item_id))
        intent = create_payment_for_item(item)  # type:ignore
        return JsonResponse({"client_secret": intent["client_secret"]})


class StripeSessionOrderView(APIView):
    """View for handle session for order"""

    def post(
        self,
        request: HttpRequest,
        **kwargs: Any,
    ) -> HttpResponse:
        order_id = kwargs.get("order_pk")
        assert isinstance(order_id, int)
        order = get_object_or_404(
            get_order(order_pk=order_id, fields=("items", "discount", "tax"))
        )
        session = create_session_for_order(request, order)  # type:ignore
        return JsonResponse({"id": session.id})


class StripeIntentOrderView(APIView):
    """View for handle payment for order"""

    def post(
        self,
        request: HttpRequest,  # pylint: disable=unused-argument
        **kwargs: Any,
    ) -> HttpResponse:
        order_id = kwargs.get("order_pk")
        assert isinstance(order_id, int)
        order = get_object_or_404(
            get_order(
                order_pk=order_id,
                fields=("discount", "tax", "unit_amount"),
            )
        )
        intent = create_payment_for_order(order)  # type:ignore
        return JsonResponse({"client_secret": intent["client_secret"]})
