from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_selling_price = serializers.ReadOnlyField(source='product.selling_price')
    class Meta:
        model = Sale
        fields = '__all__'