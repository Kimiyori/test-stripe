from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.views import APIView
from stripe_app.services.db_services import get_order
from stripe_app.services.stripe_services import (
    create_payment_for_item,
    create_payment_for_order,
    create_session_for_item,
    create_session_for_order,
)
from stripe_app.models import Item


class SuccesView(TemplateView):
    template_name: str = "success.html"


class FailView(TemplateView):
    template_name: str = "fail.html"


class ItemView(TemplateView):

    template_name = "stripe_app/item.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update(dict(item=get_object_or_404(Item, pk=kwargs.get("pk"))))
        return context


class OrderView(TemplateView):

    template_name = "stripe_app/order.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        order = get_order(kwargs.get("order_pk"))
        context.update({"order": order[0]})
        return context


class StripeSessionItemView(APIView):
    def post(self, request, **kwargs):
        session = create_session_for_item(request, request.data)
        return JsonResponse({"id": session.id})


class StripeIntentItemView(APIView):
    def post(self, request, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get("pk"))
        intent = create_payment_for_item(item)
        return JsonResponse({"client_secret": intent["client_secret"]})


class StripeSessionOrderView(APIView):
    def post(
        self,
        request,
        **kwargs,
    ):
        order = get_order(kwargs.get("order_pk"))
        session = create_session_for_order(request, order[0])
        return JsonResponse({"id": session.id})


class StripeIntentOrderView(APIView):
    def post(
        self,
        request,
        **kwargs,
    ):
        order = get_order(kwargs.get("order_pk"))
        intent = create_payment_for_order(order[0])
        return JsonResponse({"client_secret": intent["client_secret"]})
