from django.urls import path
from .views import (index, menu, about, checkout, product_by_category, detail, order_by_alphabet, order_by_alphabet_reverse,
                    order_by_price, order_by_price_2, discount, register_form, login_form, logout_user, cart, to_cart, save_comment,
                    create_checkout_session, success_payment)

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
    path('about/', about, name='about'),
    path('checkout/', checkout, name='book'),
    path('detail/<int:id>/', detail, name='detail'),

    path('comment/<int:id>/', save_comment, name='comment'),

    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('payment/', create_checkout_session, name='payment'),
    path('success-payment/', success_payment, name='success'),

    path('registration/', register_form, name='register'),
    path('login/', login_form, name='login'),
    path('logout/', logout_user, name='logout'),

    path('product/<int:id>/', product_by_category, name='product_by_category'),
    path('alphabet/', order_by_alphabet, name='alphabet'),
    path('alphabet_reverse/', order_by_alphabet_reverse, name='reverse'),
    path('price/', order_by_price, name='price'),
    path('price2/', order_by_price_2, name='price2'),
    path('discount/', discount, name='discount'),
]