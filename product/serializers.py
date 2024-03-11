from rest_framework import serializers
from .models import Product

class MySerializer(serializers.Serializer):
    PRODUCT_CHOICES = [(product.name, product.name) for product in Product.objects.all()]

    product_name1 = serializers.ChoiceField(choices=PRODUCT_CHOICES)
    quantity1 = serializers.IntegerField()
    product_name2 = serializers.ChoiceField(choices=PRODUCT_CHOICES)
    quantity2 = serializers.IntegerField()
