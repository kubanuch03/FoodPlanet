from rest_framework import serializers

from .models import Products


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['title','slug','description','category','is_have','quentity','price','image']
