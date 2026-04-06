from django.db import models
from django.conf import settings


class Transaction(models.Model):

    # Type choices
    INCOME = 'income'
    EXPENSE = 'expense'

    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    # Category choices
    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"