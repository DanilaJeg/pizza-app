from django.shortcuts import render, redirect
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
            Orders.objects.create(user=request.user, pizza=pizza)
            form.save()
            return redirect('payment')
    else:
        form = PizzaForm()
    return render(request, 'order.html', {'form': form})


def prev(request):
    curr_user = request.user.username
    pizzas = Orders.objects.all()
    context = {'user': curr_user, 'pizzas': pizzas}
    return render(request, 'previous_order.html', context)


def payment(request):
    if request.method == "POST":
        payment = PaymentForm(request.POST)
        address = AddressForm(request.POST)
        
        if payment.is_valid() and address.is_valid():
            pData = payment.cleaned_data
            aData = address.cleaned_data
            return redirect('index')
    else:
        payment = PaymentForm()
        address = AddressForm()
    return render(request, 'payment.html', {'payment': payment, 'address': address})
