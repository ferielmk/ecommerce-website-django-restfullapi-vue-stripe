
from django.urls import path, include

from product import views
from rest_framework.routers import DefaultRouter
from .views import WishViewSet
router = DefaultRouter()
router.register('wish-gestion', WishViewSet, basename='wish-gestion')


urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('categories-list/', views.CategoriesList.as_view()),
    
    path('brands-list/', views.BrandsList.as_view()),
    path('products/wishDelete/<int:product_id>/', views.removeFromWishList),
    path('products/wishAdd/', views.addToWishList),
    path('products/wish/', views.WishListProducts.as_view()),
    
    #put urls with slugs after or it will consider 'products/search' as 'products/<slug:category_slug>/' where '<slug:category_slug>' = 'search'
    path('products/category-brand/<slug:category_slug>/<slug:brand_slug>/', views.BrandCatDetail.as_view()),
    path('products/category-brand-product/<slug:category_slug>/<slug:brand_slug>/<slug:product_slug>/', views.ProductBrandDetail.as_view()),
    path('products/category-product/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    
    #test
    #path('user-info/', views.user_info, name='user_info'),
    path('superuser/<int:pk>/', views.SuperuserDetailView.as_view(), name='superuser-detail'),
    path('superusers/', views.SuperuserListView.as_view(), name='superuser-list'),
    path('Dashboard2/', views.CategoryCount.as_view()),
    path('totalproducts/', views.TotalProducts.as_view()),
    path('', include(router.urls)),
] 