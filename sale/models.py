from django.db import models
from product.models import Product

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    date = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)