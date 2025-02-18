from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('order/', views.order, name='order'),
    path('payment/', views.payment, name='payment'),
    path('previous_order/', views.prev, name='previous_orders'),
    path('order_complete/<int:order_id>', views.order_complete, name='order_complete'),
    path('logout/', LogoutView.as_view(next_page="/"), name="logout"),
    path('pizza_cart/', views.cart, name="cart"),
    path('cart/remove/<int:pizza_id>/',views.remove_from_cart, name='remove_from_cart'),
]