from django.contrib import admin
from .models import Register, Product

# Register your models here.

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ("id","full_name","email","mobile","created_at",'password')

    search_fields = ("full_name","email","mobile", )

    list_filter = ( "created_at",    )

    ordering = ("-created_at",)

    list_per_page = 10

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","category","gender","price","stock","created_at","size","color","brand","sku"   )

    search_fields = ("name","category","brand")

    list_filter = ("category","gender","created_at")

    ordering = ("-created_at",)

    list_per_page = 10