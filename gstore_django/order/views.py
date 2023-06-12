import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum
from django.db.models import Count

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer



@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = 0
        for item in serializer.validated_data['items']:
            if(item.get('product').price_sale !=0):
                paid_amount = paid_amount+(item.get('quantity') * item.get('product').price_sale)
            else:
                paid_amount = paid_amount+(item.get('quantity') * item.get('product').price)

        try:
            # for item in serializer.validated_data['items']:
            #     print(item.get('product').quantity) 
            
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from GStore',
                source=serializer.validated_data['stripe_token']
            )
            #save data
            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    


# Quantite par produits
#GRAPHE

class OrderProductData(APIView):


    def get(self, request, format=None):
        product_data = OrderItem.objects.values('product').annotate(total_quantity=Sum('quantity'))
        labels = [item['product'] for item in product_data]
        data = [item['total_quantity'] for item in product_data]
        response_data = {'labels': labels, 'data': data}
        return Response(response_data)



        

# Nombre de catégories
#pas de graphe

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        response_data = {'orders': serializer.data}
        return Response(response_data)


#Nombres d'utilisateurs connectés a la base de données, User's model is provided by Django's built-in authentication system
#pas de graphe 

class users_count(APIView):
    def get(self, request, format=None):
         registered_users_count = User.objects.count()
         return Response(registered_users_count)

#commandes par categorie 
#Graphe
    
class commandes_par_cateorie(APIView):
    def get(self,request, format=None):
        category_counts = OrderItem.objects.values('product__category__name').annotate(count=Count('order'))
        response_data = [{'category': item['product__category__name'], 'count': item['count']} for item in category_counts] 
        return Response(response_data)


#Nombre total de produits achetes
#pas de graphe
class total_produits_achetes(APIView):
    def get(self, request, format=None):
        total_quantity = OrderItem.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        response_data = {'total_quantity': total_quantity}
        print(response_data)
        return Response(response_data)
    

