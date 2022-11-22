from django.urls import path
from .views import (
    StripeIntentOrderView,
    StripeSessionItemView,
    ItemView,
    StripeSessionOrderView,
    StripeIntentItemView,
    OrderView,
    SuccesView,
    FailView,
)

urlpatterns = [
    path("item/<int:pk>", ItemView.as_view(), name="get_item"),
    path("order/<int:order_pk>", OrderView.as_view(), name="get_order"),
    path(
        "buy/session/<int:pk>",
        StripeSessionItemView.as_view(),
        name="create_session_item",
    ),
    path(
        "buy/intent/<int:pk>",
        StripeIntentItemView.as_view(),
        name="create_payment_intent_item",
    ),
    path(
        "order/buy/session/<int:order_pk>",
        StripeSessionOrderView.as_view(),
        name="create_session_order",
    ),
    path(
        "order/buy/intent/<int:order_pk>",
        StripeIntentOrderView.as_view(),
        name="create_payment_order",
    ),
    path("success", SuccesView.as_view(), name="success"),
    path("fail", FailView.as_view(), name="fail"),
]
