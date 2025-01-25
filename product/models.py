from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_stock = models.IntegerField()
    unit_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def pieces_sold(self):
        return sum(sale.quantity_sold for sale in self.sale_set.all())

    @property
    def pieces_pending(self):
        return self.total_stock - self.pieces_sold

    @property
    def total_investment(self):
        return (self.unit_purchase_price + self.unit_taxes) * self.total_stock

    @property
    def expected_return(self):
        return (self.selling_price - (self.unit_purchase_price + self.unit_taxes)) * self.total_stock

    @property
    def profit(self):
        return self.selling_price - (self.unit_purchase_price + self.unit_taxes)

    def __str__(self):
        return self.name
