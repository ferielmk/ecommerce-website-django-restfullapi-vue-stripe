from django.urls import path

from order import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('orders/', views.OrdersList.as_view()),  
    path('Dashboard/', views.OrderProductData.as_view()),
    path('Dashboard/userscount/',views.users_count.as_view()),
    path('Dasboard/category-counts/',views.commandes_par_cateorie.as_view(), name='category-counts'),
    path('Dasboard/total-products/', views.total_produits_achetes.as_view(), name='total-products'),
    
]