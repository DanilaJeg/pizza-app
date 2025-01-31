from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('order/', views.order, name='order'),
    path('payment/<int:pizza>/', views.payment, name='payment'),
    path('previous_order/', views.prev, name='previous_orders'),
    path('order_complete/<int:order_id>', views.order_complete, name='order_complete'),
]