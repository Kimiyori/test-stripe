from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from stripe_app.services.db_services import get_order
from stripe_app.services.stripe_services import (
    create_session_for_item,
    create_session_for_order,
)
from stripe_app.models import Item


def success(request):
    return render(request, "stripe_app/success.html")


def fail(request):
    return render(request, "stripe_app/fail.html")


class ItemView(TemplateView):

    template_name = "stripe_app/item.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context.update(dict(item=get_object_or_404(Item, pk=kwargs.get("pk"))))
        return context


class BuyItemAPIView(APIView):
    def get(self, request, **kwargs):
        item = get_object_or_404(Item, pk=kwargs.get("pk"))
        session = create_session_for_item(request, item)
        return JsonResponse({"session_id": session.id})


class OrderView(TemplateView):

    template_name = "stripe_app/order.html"
    extra_context = {"stripe_api_key": settings.STRIPE_PUBLIC_KEY}

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        order = get_order(kwargs.get("order_pk"))
        context.update({"order": order[0]})
        return context


class BuyOrderAPIView(APIView):
    def get(
        self,
        request,
        **kwargs,
    ):
        order = get_order(kwargs.get("order_pk"))
        session = create_session_for_order(request, order[0])
        return JsonResponse({"session_id": session.id})
