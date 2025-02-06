from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import PizzaForm, PaymentForm, AddressForm
from .models import Orders, Pizza, Cart
from django.contrib.auth.decorators import login_required

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
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save()

            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.pizzas.add(pizza)

            return redirect('cart')
    else:
        form = PizzaForm()
    return render(request, 'order.html', {'form': form})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    pizzas = cart.pizzas.all()

    if request.method == "POST":
        if "checkout" in request.POST:
            return redirect("payment")
    return render(request, 'cart.html', {"cart": cart, "pizzas": pizzas})

@login_required
def remove_from_cart(request, pizza_id):
    cart = get_object_or_404(Cart, user=request.user)  
    pizza = get_object_or_404(Pizza, id=pizza_id)  
    if cart.user != request.user:
        return redirect('/')

    if cart.pizzas.filter(id=pizza.id).exists():
        cart.pizzas.remove(pizza)
        pizza.delete()

    return redirect('cart')

@login_required
def prev(request):
    curr_user = request.user
    orders = Orders.objects.filter(user=curr_user).order_by("-id")
    context = {'user': curr_user, 'orders': orders}
    return render(request, 'previous_order.html', context)


@login_required
def payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    pizzas = cart.pizzas.all()

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST)
        
        if payment_form.is_valid() and address_form.is_valid():

            # order is only placed after payment. 
            address = address_form.save()
            order = Orders.objects.create(user=request.user, address=address)
            order.pizza.set(pizzas)
            order.save()

            cart.pizzas.clear()
            return redirect('order_complete', order.id)
    else:
        payment_form = PaymentForm()
        address_form = AddressForm()
    return render(request, 'payment.html', {'payment': payment_form, 'address': address_form})

@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    if order.user != request.user:
        return redirect('/')
    return render(request, 'order_complete.html', {"order": order})