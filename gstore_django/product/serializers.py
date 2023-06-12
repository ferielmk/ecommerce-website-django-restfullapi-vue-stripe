from rest_framework import serializers

from .models import Category, Product, Brand, Sale, Wish

# nesrine changed modified/created_at_read to not pass the attrs to frontend only when we need to read them
# modified models for this
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = (
            "created_at",
            "modified_at"
        ),
        created_at_read = serializers.ReadOnlyField()
        modified_at_read = serializers.ReadOnlyField()
        slug_at_read = serializers.ReadOnlyField()
        brand_name = serializers.ReadOnlyField()
        category_name = serializers.ReadOnlyField()
        
        
        fields = (
            "id",
            "brand",
            "category",
            "brand_name",
            "category_name",
            "name",
            
            "get_absolute_url",
            "description",
            "price",
            "price_sale",
            "quantity", #idk if we need this
            "image",
            "get_image",
            "get_thumbnail",
            "created_at_read",
            "modified_at_read",
            "slug_at_read"
            
        )
        
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    read_only_fields = (
            "created_at",
            "modified_at"
        ),
    created_at_read = serializers.ReadOnlyField()
    modified_at_read = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            "created_at_read",
            "modified_at_read"
            
        )
    
    
class WishSerializer(serializers.ModelSerializer):
    read_only_fields = (
            "created_at"
        ),
    product_name = serializers.ReadOnlyField()
    class Meta:
        model = Wish
        fields = (
            "user",
            "product",
            "created_at",
            "product_name"
        )


    
class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        read_only_fields = (
            "created_at",
            "modified_at"
        ),
        created_at_read = serializers.ReadOnlyField()
        modified_at_read = serializers.ReadOnlyField()
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            "created_at_read",
            "modified_at_read"
        )

#nesrine
from django.db.models import F  
class SaleSerializer(serializers.ModelSerializer):
    read_only_fields = (
            "created_at",
            "modified_at"
        ),
    created_at_read = serializers.ReadOnlyField()
    modified_at_read = serializers.ReadOnlyField()
    class Meta:
        model = Sale
        fields = (
            "id",
            "sale_value",
            "created_at_read",
            "modified_at_read"
        )
    #nesrine
    def validate(self, value):
        """
        Check that the sale is not in the database.
        """
        print(value)
        instance = getattr(self, 'instance', None)
        if instance is None and Sale.objects.exists():
            raise serializers.ValidationError("A Sale already exists in the database.")
        return value
    #overwrite create
    #validated_data from the chackout form
    def create(self, validated_data):
        # Get sale value from validated data
        sale_value = validated_data.get('sale_value')

        # Update all product sale prices
        Product.objects.update(price_sale=F('price') * (1 - sale_value / 100))

        # Create new sale object
        sale = Sale.objects.create(**validated_data)

        return sale
    def update(self, instance, validated_data):
        # First, update the Sale instance
        instance = super().update(instance, validated_data)

        # Then, update the prices of all products
        sale_value = validated_data.get('sale_value')
        Product.objects.update(price_sale=F('price') * (1 - sale_value / 100))

        return instance
        
    
     
from django.contrib.auth.models import User
from rest_framework import serializers

class SuperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser')