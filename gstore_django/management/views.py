from django.shortcuts import render
from django.db.models import Q
from product.models import Product, Category, Sale, Brand
from product.serializers import ProductSerializer, CategorySerializer, SaleSerializer, BrandSerializer
# Create your views here.

#for crud operations
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.decorators import api_view

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    print(queryset)
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    print(queryset)
    
class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    print(queryset)
    
class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    print(queryset)
    

    
@api_view(['POST'])
def delete_product(request, product_id):
    product = Product.objects.filter(pk=product_id)
    
    product.delete()

    return Response({'message': 'The product was deleted'})

@api_view(['POST'])
def delete_category(request, category_id):
    category = Category.objects.filter(pk=category_id)
    
    category.delete()

    return Response({'message': 'The category was deleted'})

@api_view(['POST'])
def delete_brand(request, brand_id):
    brand = Brand.objects.filter(pk=brand_id)
    
    brand.delete()

    return Response({'message': 'The brand was deleted'})

@api_view(['POST'])
def delete_sale(request, sale_id):
    sale = Sale.objects.filter(pk=sale_id)
    #put all sale prices of all products to null
    
    Product.objects.update(price_sale=None)
    
    sale.delete()

    return Response({'message': 'The sale was deleted'})

@api_view(['POST'])    
def sale_exists(request):
    if Sale.objects.exists():
        sale = Sale.objects.first()
        return Response({'value': 'true', 'sale_value': sale.sale_value})
    return Response({'value': 'false'})

@api_view(['POST'])
def search_products(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query)| Q(category__name__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def search_categories(request):
    query = request.data.get('query', '')

    if query:
        categories = Category.objects.filter(Q(name__icontains=query))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    else:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def search_brands(request):
    query = request.data.get('query', '')

    if query:
        brands = Brand.objects.filter(Q(name__icontains=query) )
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
    else:
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)