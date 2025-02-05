from django.db import models
from product.models import Product
from django.db.models import Sum, F


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    date = models.CharField(max_length=255)  # Format: "2025-W06" or "2025-02"
    notes = models.TextField(null=True, blank=True)
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_weekly_sales(cls, user, year=None, week=None):
        queryset = cls.objects.filter(created_by=user)
        
        if year and week:
            week_format = f"{year}-W{week:02d}"
            queryset = queryset.filter(date=week_format)
        
        return queryset.values(
            'date',
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity_sold'),
            total_amount=Sum(F('quantity_sold') * F('product__selling_price'))
        ).order_by('date')

    @classmethod
    def get_monthly_sales(cls, user, year=None, month=None):
        queryset = cls.objects.filter(created_by=user)
        
        if year and month:
            queryset = queryset.filter(
                created_at__year=year,
                created_at__month=month
            )
        
        return queryset.values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity_sold'),
            total_amount=Sum(F('quantity_sold') * F('product__selling_price'))
        ).order_by('product__name')