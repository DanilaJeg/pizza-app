from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import datetime


# Create your models here.
class Size(models.Model):
    size = models.CharField(max_length=50, default="Medium")
    price = models.FloatField(default=11.50)

    def __str__(self):
        return self.size

class Crust(models.Model):
    crust = models.CharField(max_length=50, default="Normal")
    price = models.FloatField(default=0)

    def __str__(self):
        return self.crust

class Base(models.Model):
    base = models.CharField(max_length=50, default="Regular")
    price = models.FloatField(default=1.0)

    def __str__(self):
        return self.base

class Topping(models.Model):
    topping = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.topping

class Cheese(models.Model):
    cheese = models.CharField(max_length=50, default="Mozarella")
    price = models.FloatField(default=0.5)

    def __str__(self):
        return self.cheese

class Pizza(models.Model):
    # for the topping to pizza relationship. I chose many to many
    # i feel the many to many relationship is the best choice here as a pizza can have many toppings and a topping can be on many pizzas.
    # i thought of maybe making the toppings a many to one relationship but i feel that wouldnt be the best choice as a topping can be on many pizzas.
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping, blank=True, default=None)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)

    def allToppings(self):
        return [t.topping for t in self.topping.all()]

    def totalPrice(self):
        toppings = sum(t.price for t in self.topping.all())
        return self.size.price + self.crust.price + self.base.price + toppings + self.cheese.price

    def __str__(self):
        toppings = [t.topping for t in self.topping.all()]
        string_toppings = ", ".join(toppings)
        return f"{self.size} pizza with {self.crust} crust and {self.base} base. With the following toppings: {string_toppings}."

class Address(models.Model):
    COUNTIES = [
        ('Antrim', 'Antrim'), ('Armagh', 'Armagh'), ('Carlow', 'Carlow'), ('Cavan', 'Cavan'),
        ('Clare', 'Clare'), ('Cork', 'Cork'), ('Derry', 'Derry'), ('Donegal', 'Donegal'),
        ('Down', 'Down'), ('Dublin', 'Dublin'), ('Fermanagh', 'Fermanagh'), ('Galway', 'Galway'),
        ('Kerry', 'Kerry'), ('Kildare', 'Kildare'), ('Kilkenny', 'Kilkenny'), ('Laois', 'Laois'),
        ('Leitrim', 'Leitrim'), ('Limerick', 'Limerick'), ('Longford', 'Longford'), ('Louth', 'Louth'),
        ('Mayo', 'Mayo'), ('Meath', 'Meath'), ('Monaghan', 'Monaghan'), ('Offaly', 'Offaly'),
        ('Roscommon', 'Roscommon'), ('Sligo', 'Sligo'), ('Tipperary', 'Tipperary'), ('Tyrone', 'Tyrone'),
        ('Waterford', 'Waterford'), ('Westmeath', 'Westmeath'), ('Wexford', 'Wexford'), ('Wicklow', 'Wicklow')
    ]

    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=50, choices=COUNTIES)
    town = models.CharField(max_length=50)
    eircode = models.CharField(max_length=8)

    def __str__(self):
        if self.address2 is not None:
            return f"{self.name}, {self.address1}, {self.address2},{self.town}, {self.county}, {self.eircode}"
        else:
            return f"{self.name}, {self.address1}, {self.town}, {self.county}, {self.eircode}"

class Cart(models.Model):
    # pizzas can be on many carts and a cart can have many pizzas. So i chose many to many relationship.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)

    def total_price(self):
        return sum(pizza.totalPrice() for pizza in self.pizzas.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class Orders(models.Model):
    # for the pizza to order relationship. I chose many to many as a pizza can be on many orders and an order can have many pizzas.
    # altough i did try and implement a one to many relationship but i feel that wouldnt be the best choice as a pizza can be on many orders.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    pizza = models.ManyToManyField(Pizza)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def total_price(self):
        return sum(p.totalPrice() for p in self.pizza.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Payment(models.Model):
     # im using char field for card number and cvv as it is easier to validate, and i can use regex to validate the input in the form.
     # also making it a char field i can allow a maximum amount of digits to be entered. So they can only go up to 16 digits for card number and 3 digits for cvv.
     # i am also using a regex validator to make sure that only numbers are entered into the fields. In the form. 
    today = datetime.today()
    cardHolder = models.CharField(max_length=50)
    cardNumber = models.CharField(max_length=16)
    expiration_month = models.IntegerField(validators=[MinValueValidator(today.month), MaxValueValidator(12)])
    expiration_year = models.IntegerField(validators=[MinValueValidator(today.year), MaxValueValidator(today.year + 10)])
    cvv = models.CharField(max_length=3)

