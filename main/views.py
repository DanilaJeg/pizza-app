from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import PizzaForm, PaymentForm, AddressForm
from .models import Orders, Pizza

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("order")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('previous_orders')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


def order(request):
    if request.method == "POST":
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()
            return redirect('payment', pizza=pizza.id)
    else:
        form = PizzaForm()
    return render(request, 'order.html', {'form': form})


def prev(request):
    curr_user = request.user
    pizzas = Orders.objects.filter(user=curr_user)
    context = {'user': curr_user, 'pizzas': pizzas}
    return render(request, 'previous_order.html', context)


def payment(request, pizza):
    pizza = get_object_or_404(Pizza, id=pizza)

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST)
        
        if payment_form.is_valid() and address_form.is_valid():
            # order is only placed after payment. 
            address = address_form.save()
            order = Orders.objects.create(user=request.user, pizza=pizza, address=address)
            order.save()

            return redirect('order_complete', order.id)
    else:
        payment_form = PaymentForm()
        address_form = AddressForm()
    return render(request, 'payment.html', {'payment': payment_form, 'address': address_form})

def order_complete(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    toppings = order.pizza.allToppings()
    return render(request, 'order_complete.html', {"order": order, "toppings": toppings})
