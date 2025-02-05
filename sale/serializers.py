from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_selling_price = serializers.ReadOnlyField(source='product.selling_price')
    class Meta:
        model = Sale
        fields = '__all__'


class SalesReportSerializer(serializers.Serializer):
    date = serializers.CharField()
    product__name = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)