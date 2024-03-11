from django.db import models
import uuid


class Product(models.Model):
    name = models.CharField(max_length=128)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='PM_product')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='PM_materials')
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product.name} -{self.material} - miqdor: {self.quantity}"

class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='W_materials')
    remainder = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.material} - qolgan: {self.remainder} - narxi:{self.price} dan"
