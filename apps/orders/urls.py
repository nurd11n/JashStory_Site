from django.urls import path
from .views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='create'),
    path('', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]