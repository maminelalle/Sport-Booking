from django.contrib import admin
from .models import Payment, Invoice

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'amount', 'currency', 'method', 'status', 'created_at']
    list_filter = ['status', 'method', 'currency', 'created_at']
    search_fields = ['reservation__id', 'stripe_payment_intent_id', 'transaction_reference']
    readonly_fields = ['created_at', 'updated_at', 'paid_at']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'payment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['invoice_number', 'payment__id']
    readonly_fields = ['invoice_number', 'created_at', 'updated_at']
