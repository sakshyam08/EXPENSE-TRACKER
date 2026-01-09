from django.contrib import admin
from tracker.models import *
# Register your models here.
admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"

admin.site.register(CurrentBalance)

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description','expense_type')

admin.site.register(TrackingHistory, TrackingHistoryAdmin)