from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.TextChoices):
    ELECTRONICS = "Electronics"
    LAPTOPS = "Laptops"
    ARTS = "Arts"
    FOOD = "Food"
    HOME = "Home"
    KITCHEN = "Kitchen"


class Product(models.Model):

    name = models.CharField(max_length=200, default="", blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=False)
    category = models.CharField(max_length=30, choices=Category.choices)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class Profile(models.Model):
#     name = models.CharField(max_length=30, default="")
#     profile_image = models.ImageField(upload_to="Image", blank=False)
#     user_file = models.FileField(upload_to="File", blank=False)


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="image"
    )
    image = models.ImageField(upload_to="product_images")
