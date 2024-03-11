from rest_framework import serializers

import warehouse
from product.models import Product, Warehouse

class MySerializer(serializers.Serializer):
    product_name = serializers.CharField(required=True, help_text="Name of the product",max_length=32)
    quantity = serializers.IntegerField(required=True, help_text="Quantity of the product")
