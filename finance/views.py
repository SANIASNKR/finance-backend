from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from users.permissions import IsAnalystOrAdmin, IsAdmin


class TransactionListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only analyst and admin can create
            return [IsAnalystOrAdmin()]
        # Anyone logged in can view
        return [IsAuthenticated()]

    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-date')

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TransactionDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'DELETE':
            # Only admin can delete
            return [IsAdmin()]
        if self.request.method == 'PATCH':
            # Only analyst and admin can edit
            return [IsAnalystOrAdmin()]
        # Anyone logged in can view
        return [IsAuthenticated()]

    def get_object(self, pk, user):
        try:
            return Transaction.objects.get(pk=pk, user=user)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)

        if transaction is None:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def patch(self, request, pk):
        transaction = self.get_object(pk, request.user)

        if transaction is None:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)

        if transaction is None:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        transaction.delete()
        return Response(
            {'message': 'Transaction deleted successfully'},
            status=status.HTTP_200_OK
        )