from rest_framework import viewsets
from product.models import Product
from rest_framework.response import Response

class TotalsViewSet(viewsets.ViewSet):
    def list(self, request):
        total_investment = sum(product.total_investment for product in Product.objects.all())
        expected_return = sum(product.expected_return for product in Product.objects.all())
        profit = sum(product.total_profit for product in Product.objects.all())
        pieces_sold = sum(product.pieces_sold for product in Product.objects.all())
        pieces_pending = sum(product.pieces_pending for product in Product.objects.all())
        total_revenue = sum(product.total_revenue for product in Product.objects.all())

        return Response({
            'total_investment': total_investment,
            'expected_return': expected_return, 
            'profit': profit,
            'pieces_sold': pieces_sold,
            'pieces_pending': pieces_pending,
            'total_revenue': total_revenue
        })