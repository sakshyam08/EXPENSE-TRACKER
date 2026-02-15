from django.shortcuts import render
#from httpcore import request
from .models import CurrentBalance, TrackingHistory
from django.shortcuts import redirect
from decimal import Decimal as decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login

from django.contrib import messages
# Create your views here.
from decimal import Decimal




def login_view(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not username or not password:
            messages.error(request, "Username and Password are required")
            return redirect('register')

        if User.objects.filter(username=username).exists():
           
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, "User created successfully")
        return redirect('login')

    return render(request, 'register.html')

def logout(request):
    
    messages.success(request, "Logged out successfully")
    return redirect('login')

@login_required(login_url='login')
def index(request):
    print(request.user.username)
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
