from django.contrib import admin
from .models import Products, Category, CartItem




class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'quantity',
        'price',

    )

    fieldsets = (
        # (None, {"fields": ("email", "password")}),
        (
            "info",
            {
                "fields": (
                    "user",
                    "product",
                    "quantity",
                    "price",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "product",
                    "quentity",
                    
                ),
            },
        ),
    )


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'category',
        'quentity',
        'price',
        'is_have',
 
    )



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
     

    )

admin.site.register(CartItem, CartItemAdmin)

