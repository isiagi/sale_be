from rest_framework import viewsets, permissions
from .serializers import SaleSerializer, SalesReportSerializer
from .models import Sale
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum, F

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

    @action(detail=False, methods=['get'])
    def weekly_report(self, request):
        now = timezone.now()
        year = request.query_params.get('year', now.year)
        week = request.query_params.get('week', now.strftime('%V'))
        
        try:
            year = int(year)
            week = int(week)
        except (TypeError, ValueError):
            return Response({"error": "Invalid year or week format"}, status=400)

        weekly_sales = Sale.get_weekly_sales(request.user, year, week)
        serializer = SalesReportSerializer(weekly_sales, many=True)
        
        total_quantity = sum(item['total_quantity'] for item in weekly_sales)
        total_amount = sum(item['total_amount'] for item in weekly_sales)
        
        return Response({
            'period': f"{year}-W{week:02d}",
            'sales': serializer.data,
            'summary': {
                'total_quantity': total_quantity,
                'total_amount': total_amount
            }
        })

    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        now = timezone.now()
        year = request.query_params.get('year', now.year)
        month = request.query_params.get('month', now.month)
        
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12")
        except (TypeError, ValueError) as e:
            return Response({"error": str(e)}, status=400)

        monthly_sales = Sale.get_monthly_sales(request.user, year, month)
        serializer = SalesReportSerializer(monthly_sales, many=True)
        
        total_quantity = sum(item['total_quantity'] for item in monthly_sales)
        total_amount = sum(item['total_amount'] for item in monthly_sales)
        
        return Response({
            'period': f"{year}-{month:02d}",
            'sales': serializer.data,
            'summary': {
                'total_quantity': total_quantity,
                'total_amount': total_amount
            }
        })
    

    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        now = timezone.now()
        year = request.query_params.get('year', now.year)
        month = request.query_params.get('month', now.month)
        
        try:
            year = int(year)
            month = int(month)
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1 and 12")
        except (TypeError, ValueError) as e:
            return Response({"error": str(e)}, status=400)

        monthly_sales = Sale.get_monthly_sales(request.user, year, month)
        
        # Convert QuerySet to list for manipulation
        sales_list = list(monthly_sales)
        
        # Calculate totals
        total_quantity = sum(item['total_quantity'] for item in sales_list)
        total_amount = sum(item['total_amount'] for item in sales_list)
        
        # Add the month to each sales record
        for item in sales_list:
            item['date'] = f"{year}-{month:02d}"
        
        return Response({
            'period': f"{year}-{month:02d}",
            'sales': sales_list,
            'summary': {
                'total_quantity': total_quantity,
                'total_amount': total_amount
            }
        })

    @action(detail=False, methods=['get'])
    def sales_dashboard(self, request):
        """Get comprehensive sales statistics"""
        now = timezone.now()
        
        # Get current month's sales
        current_month_sales = Sale.objects.filter(
            created_by=request.user,
            created_at__year=now.year,
            created_at__month=now.month
        ).aggregate(
            total_quantity=Sum('quantity_sold'),
            total_amount=Sum(F('quantity_sold') * F('product__selling_price'))
        )
        
        # Get previous month's sales
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        
        previous_month_sales = Sale.objects.filter(
            created_by=request.user,
            created_at__year=prev_year,
            created_at__month=prev_month
        ).aggregate(
            total_quantity=Sum('quantity_sold'),
            total_amount=Sum(F('quantity_sold') * F('product__selling_price'))
        )
        
        return Response({
            'current_month': {
                'period': f"{now.year}-{now.month:02d}",
                'total_quantity': current_month_sales['total_quantity'] or 0,
                'total_amount': current_month_sales['total_amount'] or 0
            },
            'previous_month': {
                'period': f"{prev_year}-{prev_month:02d}",
                'total_quantity': previous_month_sales['total_quantity'] or 0,
                'total_amount': previous_month_sales['total_amount'] or 0
            }
        })