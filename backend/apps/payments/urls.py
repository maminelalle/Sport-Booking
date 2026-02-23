"""
URLs pour la gestion des paiements.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, InvoiceViewSet, stripe_webhook

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

app_name = 'payments'

urlpatterns = [
    path('', include(router.urls)),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]
