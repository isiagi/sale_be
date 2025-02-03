from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    total_stock = models.IntegerField()
    unit_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('category.Category', on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.SET_NULL, null=True)
    reorder_point = models.PositiveIntegerField(null=True, blank=True, default=10)
    image = CloudinaryField('image', null=True, blank=True, resource_type='image', transformation={
        'quality': 'auto',
        'fetch_format': 'auto',
    })
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

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
    def profit(self):
        return self.selling_price - (self.unit_purchase_price + self.unit_taxes)

    @property
    def expected_return(self):
        return ((self.profit * self.total_stock) - self.total_investment)
 
    @property
    def total_cost(self):
        return self.unit_purchase_price * self.total_stock
    
    @property
    def total_taxes(self):
        return self.unit_taxes * self.total_stock
    
    @property
    def total_profit(self):
        return self.profit * self.total_stock
    
    @property
    def total_selling_price(self):
        return self.selling_price * self.total_stock
    
    @property
    def total_revenue(self):
        return self.total_selling_price
    
    @property
    def total_profit_percentage(self):
        return (self.total_profit / self.total_cost) * 100
    
    @property
    def total_taxes_percentage(self):
        return (self.total_taxes / self.total_cost) * 100
    
    @property
    def total_cost_percentage(self):
        return (self.total_cost / self.total_cost) * 100
    

    def __str__(self):
        return self.name
