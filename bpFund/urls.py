from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("donate/", views.donate, name="donate"),
    path("starp/", views.starp, name="starp"),
    path("createProject/", views.createProject, name="createProject"),

    path("product_detail/<int:product_id>/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.show_cart, name="show_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("paypal/", include('paypal.standard.ipn.urls')),
    path("process_payment/", views.process_payment, name="process_payment"),
    path("payment_done/", views.payment_done, name="payment_done"),
    path("payment_cancelled/", views.payment_cancelled, name="payment_cancelled")
]