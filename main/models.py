from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Size(models.Model):
    size = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.size

class Crust(models.Model):
    crust = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.crust

class Base(models.Model):
    base = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.base

class Topping(models.Model):
    topping = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.topping

class Cheese(models.Model):
    cheese = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.cheese

class Pizza(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    topping = models.ManyToManyField(Topping, blank=True)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)

    def totalPrice(self):
        toppings = sum(t.price for t in self.topping.all())
        return self.size.price + self.crust.price + self.base.price + toppings + self.cheese.price

    def __str__(self):
        toppings = [t.topping for t in self.topping.all()]
        return f"{self.size} pizza with {self.crust} crust and {self.base} base. Toppings: {toppings}."
    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ordered pizza {self.pizza}"