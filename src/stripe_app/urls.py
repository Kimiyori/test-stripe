from django.urls import path
from stripe_app.views import (
    BuyOrderAPIView,
    ItemView,
    BuyItemAPIView,
    OrderView,
    success,
    fail,
)

urlpatterns = [
    path("item/<int:pk>", ItemView.as_view(), name="get_item"),
    path("buy/<int:pk>", BuyItemAPIView.as_view(), name="buy_item"),
    path("order/<int:order_pk>", OrderView.as_view(), name="get_order"),
    path("order/<int:order_pk>/buy/", BuyOrderAPIView.as_view(), name="buy_order"),
    path("success", success, name="success"),
    path("fail", fail, name="fail"),
]
