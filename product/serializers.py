from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    pieces_sold = serializers.ReadOnlyField()
    pieces_pending = serializers.ReadOnlyField()
    total_investment = serializers.ReadOnlyField()
    expected_return = serializers.ReadOnlyField()
    total_profit = serializers.ReadOnlyField()
    total_revenue = serializers.ReadOnlyField()
    total_cost = serializers.ReadOnlyField()
    total_taxes = serializers.ReadOnlyField()
    profit = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('total_investment', 'expected_return', 'profit', 'pieces_sold', 'pieces_pending', 'category_name', 'supplier_name', 'total_revenue', 'total_cost', 'total_taxes')