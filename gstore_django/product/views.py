from django.db.models import Q
from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

#auth
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import SuperuserSerializer

from rest_framework import status, authentication, permissions

from .models import Product, Category,Wish,Brand
from .serializers import ProductSerializer,BrandSerializer, CategorySerializer, WishSerializer
from rest_framework import viewsets

class WishViewSet(viewsets.ModelViewSet):
    serializer_class = WishSerializer
    queryset = Wish.objects.all()


#display latest products
@permission_classes([])
class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


#display categories  
@permission_classes([])
class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@permission_classes([])
class BrandsList(APIView):
    def get(self, request, format=None):
        brand = Brand.objects.all()
        serializer = BrandSerializer(brand, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class WishListProducts(APIView):
    def get(self, request, format=None):
        product = Wish.objects.filter(user=request.user)
        serializer = WishSerializer(product, many=True)
        return Response(serializer.data)


#show one product
@permission_classes([])
class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            #get the product (slug) inside a category (slug)
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data) 


@permission_classes([])
class ProductBrandDetail(APIView):
    def get_object(self, brand_slug, category_slug, product_slug):
        try:
            #get the product (slug) inside a category (slug)
            return Product.objects.filter(brand__slug = brand_slug, category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    def get(self, request, brand_slug, category_slug, product_slug, format=None):
        product = self.get_object(brand_slug, category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data) 
  
#show one category
@permission_classes([])
class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@permission_classes([])
class BrandCatDetail(APIView):
    def get(self,request, category_slug, brand_slug, format = None):
        try:
            category = Category.objects.get(slug = category_slug)
            print(category)
            brand = Brand.objects.get(slug = brand_slug)
            print(brand)
            products = Product.objects.filter(category = category, brand = brand)
            print(products)
            serializer = ProductSerializer(products, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except(Category.DoesNotExist, Brand.DoesNotExist):
            raise Http404
            

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def addToWishList(request):
    serializer = WishSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save(user=request.user)  # Save the user from the request object

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def removeFromWishList(request,product_id):
    item = Wish.objects.filter(user=request.user, product = product_id)
    item.delete()
    return Response({'message': 'The product was deleted from the wishlist'})


#nesrine   
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query)| Q(category__name__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})

#return current user to check if it's a superuser in the frontend
@permission_classes([permissions.IsAuthenticated])
class SuperuserDetailView(generics.RetrieveAPIView):
    serializer_class = SuperuserSerializer

    def get_object(self):
        print(self.request.user)
        return self.request.user
    
@permission_classes([permissions.IsAuthenticated])
class SuperuserListView(generics.ListAPIView):
    serializer_class = SuperuserSerializer

    def get_queryset(self):
        return User.objects.filter(is_superuser=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
#view that checks for sold and send this data to frontend

class CategoryCount(APIView):
    def get(self, request, format=None):
        category_count = Category.objects.count()
        print("Number of categories:", category_count)
        response_data = {'count': category_count}
        return Response(response_data)
    
from django.db.models import Sum
from django.db.models import Count 
from .models import Product

class TotalProducts(APIView):
    def get(self, request, format=None):
        total_products = Product.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        response_data = {'total_quantity': total_products}
        return Response(response_data)