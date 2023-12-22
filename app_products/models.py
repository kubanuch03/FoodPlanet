from django.db import models
from django.utils.text import slugify
from app_users.models import CustomUser

from django.utils import timezone


class Products(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/%Y/%m/%d/')
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='products')
    is_have = models.BooleanField(default=True)
    quentity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.product}"
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    def save(self, *args, **kwargs):
        self.price = self.total_price  # Автоматически выставляем значение price при сохранении
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Корзины'
        verbose_name_plural = 'Корзина'


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'


