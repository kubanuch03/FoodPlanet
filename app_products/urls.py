from .views import *
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r"product-admin", ProductAdminViewSet, basename="product-admin")


urlpatterns = [
    path('product-list/', ProductUserListView.as_view(),name='product-list')


    # path('add-to-cart/<int:product_id>/', AddToCart.as_view(), name='add-to-cart'),
    # path('process-order/', ProcessOrder.as_view(), name='process-order'),
] + router.urls
