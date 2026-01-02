from django.shortcuts import render
# from httpcore import request
from .models import CurrentBalance, TrackingHistory
from django.shortcuts import redirect
from decimal import Decimal as decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404
# Create your views here.
from decimal import Decimal

def index(request):
    # Ensure there is always a CurrentBalance object
    balance_obj, created = CurrentBalance.objects.get_or_create(defaults={'balance': 0})

    if request.method == 'POST':
        description = request.POST.get('description')
        amount = Decimal(request.POST.get('amount'))  # convert string to Decimal

        # Determine type
        expense_type = 'CREDIT' if amount >= 0 else 'DEBIT'

        # Update balance
        if expense_type == 'CREDIT':
            balance_obj.balance += amount
        else:  # DEBIT
            balance_obj.balance -= abs(amount)  # subtract correctly

        balance_obj.save()

        # Create transaction
        TrackingHistory.objects.create(
            current_balance=balance_obj,
            description=description,
            amount=abs(amount),  # always store positive amounts
            expense_type=expense_type
        )

        return redirect('index')  # redirect to avoid duplicate POST

    # GET request
    transactions = TrackingHistory.objects.all().order_by('-id')  # latest first

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.expense_type == 'CREDIT')
    total_expense = sum(t.amount for t in transactions if t.expense_type == 'DEBIT')

    context = {
        'balance': balance_obj.balance,
        'income': total_income,
        'expense': total_expense,
        'transactions': transactions,
    }

    return render(request, 'index.html', context)



def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(TrackingHistory, id=transaction_id)
    
    balance_obj = transaction.current_balance

    # Adjust balance before deleting
    if transaction.expense_type == 'CREDIT':
        balance_obj.balance -= Decimal(transaction.amount)
    else:  # DEBIT
        balance_obj.balance += Decimal(transaction.amount)  # add back the expense
    balance_obj.save()

    # Delete the transaction
    transaction.delete()

    return redirect('index')  # redirect back to homepage
