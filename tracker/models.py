from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CurrentBalance(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Current Balance: {self.balance}"

class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, null=True, blank=True, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0, editable=False)
    # category = models.CharField(max_length=100)
    expense_type=models.CharField(choices=[('CREDIT','CREDIT'),('DEBIT','DEBIT')],max_length=10)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount} - {self.expense_type}"
    

class RequestLogs(models.Model):
    request_info =models.TextField ()
    request_type=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add =True)
    
    
    

