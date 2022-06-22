from django.conf import settings
from django.db import models


class Product(models.Model):

    TYPES = (
        ("vape", "Vapes"),
        ("pod", "Pods"),
        ("cigarettes", "Cigarettes"),
        ("hookah", "Hookah"),
        ("self-rolling", "Hand Rolling Tobacco"),
        ("goo", "E-liquid "),
    )
    
    title = models.CharField(max_length=100)
    category= models.CharField(choices=TYPES, max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''


class Review(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"{self.author.email}"


class LikeProduct(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False) 

        
