from django import forms
from .models import Pizza, Topping, Address 

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'topping', 'base', 'cheese']

    topping = forms.ModelMultipleChoiceField(
        queryset = Topping.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )



class PaymentForm(forms.Form):
    CARDS = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard')
    ]

    cardType = forms.ChoiceField(label="Card Type", choices=CARDS, required=True)
    cardNumber = forms.CharField(label= "Card Number", max_length=16, min_length=13, required=True)
    cardHolder = forms.CharField(label="Full Name", max_length=100, required=True)
    expiry_date = forms.DateField(label="Expiry Date", widget=forms.DateInput(attrs={'type': 'month'}), input_formats=['%Y-%m'], required=True)
    cvv = forms.CharField(label="CVV", max_length=4, min_length=3, required=True)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'county', 'town', 'eircode']