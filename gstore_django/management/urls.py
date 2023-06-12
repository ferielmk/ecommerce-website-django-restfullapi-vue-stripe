"""gstore_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, BrandViewSet, SaleViewSet, delete_product, delete_brand, delete_category, delete_sale, sale_exists, search_products, search_categories, search_brands

router = DefaultRouter()
router.register('admin-products', ProductViewSet, basename='admin-products')
router.register('admin-categories', CategoryViewSet, basename='admin-categories')
router.register('admin-brands', BrandViewSet, basename='admin-brands')
router.register('admin-sale', SaleViewSet, basename='admin-sale')

urlpatterns = [
    path('admin/products/delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('admin/brands/delete_brand/<int:brand_id>/', delete_brand, name='delete_brand'),
    path('admin/categories/delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('admin/sale/delete_sale/<int:sale_id>/', delete_sale, name='delete_sale'),
    path('admin/sale-exists/', sale_exists, name='sale-exists'),
    path('admin/products/search/', search_products),
    path('admin/brands/search/', search_brands),
    path('admin/categories/search/', search_categories),
    path('', include(router.urls)),
    
]
