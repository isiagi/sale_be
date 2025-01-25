from rest_framework import viewsets, permissions
from .serializers import SaleSerializer
from .models import Sale

# Create your views here.
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        product_id = self.request.query_params.get('product')
        date = self.request.query_params.get('date')
        if product_id:
            queryset = queryset.filter(product_id=product_id, created_by=self.request.user)
        if date:
            queryset = queryset.filter(date=date, created_by=self.request.user)
        return queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)