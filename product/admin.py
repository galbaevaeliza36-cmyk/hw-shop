from django.contrib import admin
from .models import Product, Category, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  
    fields = ('stars', 'text', 'created_at')  
    readonly_fields = ('created_at',)  


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    inlines = [ReviewInline]  

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review)