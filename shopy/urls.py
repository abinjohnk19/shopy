from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_quantity, name='update_quantity'),

    # Checkout
    path('order/', views.order_product, name='order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
    path('my-orders/', views.my_orders, name='my_orders'),
]