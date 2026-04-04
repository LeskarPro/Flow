from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionListCreateAPIView.as_view(), name='api_transaction_list'),
    path('transactions/<int:pk>/', views.TransactionDetailAPIView.as_view(), name='api_transaction_detail'),
]
