from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    pieces_sold = serializers.ReadOnlyField()
    pieces_pending = serializers.ReadOnlyField()
    total_investment = serializers.ReadOnlyField()
    expected_return = serializers.ReadOnlyField()
    profit = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('total_investment', 'expected_return', 'profit', 'pieces_sold', 'pieces_pending')