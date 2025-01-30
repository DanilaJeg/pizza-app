from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import PizzaForm
from .models import Orders, Pizza

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("previous_orders")
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

def payment(request):
    return render(request, 'payment.html')

def prev(request):
    curr_user = request.user.username
    pizzas = Orders.objects.all()
    context = {'user': curr_user, 'pizzas': pizzas}
    return render(request, 'previous_order.html', context)