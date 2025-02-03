from rest_framework import viewsets, permissions
from .serializers import ProductSerializer
from .models import Product
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.exceptions import ValidationError
import cloudinary
import cloudinary.uploader

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # return super().create(request, *args, **kwargs)
        product_data = request.data

        # Validate category_id
        # category_id = product_data.get('category')
        # if not category_id:
        #     raise ValidationError({'category_id': 'This field is required.'})

        # Validate product image
        product_image = product_data.get('image')
        if not product_image:
            raise ValidationError({'product_image': 'This field is required.'})
        
        image_file = request.FILES.get('image')

        if image_file:
            try:
                # Upload the image to Cloudinary
                upload_result = cloudinary.uploader.upload(image_file, folder="products/",
                    resource_type="auto",
                    use_filename=True,
                    unique_filename=True)
                
                if hasattr(product_data, '_mutable'):
                    product_data._mutable = True
                product_data['image'] = upload_result['secure_url']
            except Exception as e:
                return Response({'error': str(e)}, status=400)
            
        # created_by = request.user
        product_data['created_by'] = request.user.id

        serializer = self.get_serializer(data=product_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
