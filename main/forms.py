from django import forms
from .models import Pizza, Topping, Address, Payment
import datetime

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'topping', 'base', 'cheese']

    topping = forms.ModelMultipleChoiceField(
        queryset = Topping.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

class PaymentForm(forms.ModelForm):
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(datetime.datetime.now().year, datetime.datetime.now().year + 11)]

    expiration_month = forms.ChoiceField(choices=MONTH_CHOICES)
    expiration_year = forms.ChoiceField(choices=YEAR_CHOICES)

    class Meta:
        model = Payment
        fields = ['cardHolder', 'cardNumber', 'expiration_month', 'expiration_year', 'cvv']
        labels = {
            'cardHolder': 'Full Name',
            'cardNumber': 'Card Number',
            'expiration_month': 'Expiry Month',
            'expiration_year': 'Expiry Year',
            'cvv': 'CVV',
        }
        widgets = {
            'cardNumber': forms.TextInput(attrs={'pattern': '[0-9]{16}', 'title': '16 digits required', 'inputmode': 'numeric', 'max_length': 16}),
            'cvv': forms.TextInput(attrs={'pattern': '[0-9]{3}', 'title': '3 digits required', 'inputmode': 'numeric', 'max_length': 3}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'county', 'town', 'eircode']