from django.db import models
from django.conf import settings

PRODUCT_CATEGORIES = [
    ("perfumes", "Perfumes"),
    ("vaselines", "Vaselines"),
    ("bodysprays", "Body Sprays"),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(choices=PRODUCT_CATEGORIES, max_length=20)
    stock = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
