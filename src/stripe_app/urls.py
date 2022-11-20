from django.urls import path
from stripe_app.views import (
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

    path("buy/session/<int:pk>", StripeSessionItemView.as_view(), name="create_session"),
    path('buy/intent/<pk>/', StripeIntentItemView.as_view(), name='create_payment_intent'),
    
    path(
        "order/<int:order_pk>/buy/", StripeSessionOrderView.as_view(), name="create_session_order"
    ),
        path(
        "order/<int:order_pk>/buy/intent", StripeIntentOrderView.as_view(), name="create_payment_order"
    ),

    path("SuccesView", SuccesView.as_view(), name="success"),
    path("FailView", FailView.as_view(), name="fail"),
]
