from django.contrib import admin
from .models import Pizza, Size, Base, Cheese, Topping, Crust, Orders

# Register your models here.
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'price']
    search_fields = ['size']

@admin.register(Crust)
class CrustAdmin(admin.ModelAdmin):
    list_display = ['crust', 'price']
    search_fields = ['crust']

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['topping', 'price']
    search_fields = ['topping']

@admin.register(Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ['base', 'price']
    search_fields = ['base']

@admin.register(Cheese)
class CheeseAdmin(admin.ModelAdmin):
    list_display = ['cheese', 'price']
    search_fields = ['cheese']

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['size', 'crust', 'display_toppings', 'base', 'cheese', 'totalPrice']
    search_fields = ['size__name', 'crust__name']
    filter_horizontal = ['topping'] 

    def display_toppings(self, obj):
        return ", ".join([t.topping for t in obj.topping.all()])
    display_toppings.short_description = "toppings"

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user', 'pizza']