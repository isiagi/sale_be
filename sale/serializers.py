from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = Sale
        fields = '__all__'