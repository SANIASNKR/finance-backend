from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from finance.models import Transaction


class DashboardSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get only this user's transactions
        user_transactions = Transaction.objects.filter(
            user=request.user
        )

        # Calculate total income
        total_income = user_transactions.filter(
            type='income'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate total expenses
        total_expense = user_transactions.filter(
            type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate net balance
        net_balance = total_income - total_expense

        # Category wise breakdown
        category_breakdown = []

        categories = ['salary', 'food', 'transport',
                      'entertainment', 'bills', 'health', 'other']

        for category in categories:
            cat_total = user_transactions.filter(
                category=category
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

            if cat_total > 0:
                category_breakdown.append({
                    'category': category,
                    'total': cat_total
                })

        # Recent 5 transactions
        recent_transactions = user_transactions.order_by(
            '-date'
        )[:5].values(
            'id', 'amount', 'type', 'category', 'date', 'description'
        )

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'category_breakdown': category_breakdown,
            'recent_transactions': list(recent_transactions)
        })