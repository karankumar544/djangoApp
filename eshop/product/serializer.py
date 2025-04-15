from rest_framework import serializers
from .models import Product, ProductImage


class ProductSerialize(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductImageSerialize(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"
