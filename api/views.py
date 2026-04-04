from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from transactions.models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/transactions/  — list the logged-in user's transactions
    POST /api/transactions/  — create a new transaction for the logged-in user

    Supports filtering by type (?type=income or ?type=expense)
    and ordering by date or amount (?ordering=date or ?ordering=-amount).
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        transaction_type = self.request.query_params.get('type')
        if transaction_type in ['income', 'expense']:
            queryset = queryset.filter(type=transaction_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/transactions/<pk>/  — retrieve a single transaction
    PUT    /api/transactions/<pk>/  — full update
    PATCH  /api/transactions/<pk>/  — partial update
    DELETE /api/transactions/<pk>/  — delete
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only access their own transactions
        return Transaction.objects.filter(user=self.request.user)
