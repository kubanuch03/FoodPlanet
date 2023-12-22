from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,permissions,viewsets

from django.shortcuts import get_object_or_404


from .serializers import ProductSerializer
from .models import Products
from celery import Celery
# from .tasks import process_order

# class AddToCart(APIView):
#     def post(self, request, product_id):
#         product = get_object_or_404(Products, pk=product_id)

#         # Получение или создание корзины в сессии
#         cart = request.session.get('cart', {})
#         cart_item = cart.get(product_id, 0)
#         cart[product_id] = cart_item + 1
#         request.session['cart'] = cart

#         return Response({'message': 'Product added to cart'})
    



# class ProcessOrder(APIView):
#     def post(self, request):
#         cart = request.session.get('cart', {})
#         user_id = request.user.id

#         # Отправка заказа на обработку Celery
#         process_order.apply_async(args=[cart, user_id])

#         # Очистка корзины
#         request.session['cart'] = {}

#         return Response({'message': 'Order processed successfully'})
    


class ProductUserListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]



class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

