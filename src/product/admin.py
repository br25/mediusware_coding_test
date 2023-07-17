from django.contrib import admin
from .models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'active')
    search_fields = ('title', 'description')
    list_filter = ('active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'description')
    search_fields = ('title', 'sku', 'description')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'file_path')
    search_fields = ('product__title',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('variant_title', 'variant', 'product')
    search_fields = ('variant_title', 'product__title')
    list_filter = ('variant', 'product')

# @admin.register(ProductVariantPrice)
# class ProductVariantPriceAdmin(admin.ModelAdmin):
#     list_display = ('product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock', 'product')
#     search_fields = ('product__title', 'product_variant_one__variant_title', 'product_variant_two__variant_title', 'product_variant_three__variant_title')
#     list_filter = ('product', 'product_variant_one', 'product_variant_two', 'product_variant_three')

@admin.register(ProductVariantPrice)
class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display = ('display_variants', 'price', 'stock', 'product')
    search_fields = ('product__title', 'product_variant_one__variant_title', 'product_variant_two__variant_title', 'product_variant_three__variant_title')
    list_filter = ('product', 'product_variant_one', 'product_variant_two', 'product_variant_three')

    def display_variants(self, obj):
        return f"{obj.product_variant_one} / {obj.product_variant_two} /"

    display_variants.short_description = 'Variants'