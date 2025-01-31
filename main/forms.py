from django import forms
from .models import Pizza, Topping, Size, Crust, Base, Cheese

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

class AddressForm(forms.Form):
    COUNTIES = [('Antrim', 'Antrim'), ('Armagh', 'Armagh'), ('Carlow', 'Carlow'), ('Cavan', 'Cavan'),
                ('Clare', 'Clare'), ('Cork', 'Cork'), ('Derry', 'Derry'), ('Donegal', 'Donegal'),
                ('Down', 'Down'), ('Dublin', 'Dublin'), ('Fermanagh', 'Fermanagh'), ('Galway', 'Galway'),
                ('Kerry', 'Kerry'), ('Kildare', 'Kildare'), ('Kilkenny', 'Kilkenny'), ('Laois', 'Laois'),
                ('Leitrim', 'Leitrim'), ('Limerick', 'Limerick'), ('Longford', 'Longford'), ('Louth', 'Louth'),
                ('Mayo', 'Mayo'), ('Meath', 'Meath'), ('Monaghan', 'Monaghan'), ('Offaly', 'Offaly'),
                ('Roscommon', 'Roscommon'), ('Sligo', 'Sligo'), ('Tipperary', 'Tipperary'), ('Tyrone', 'Tyrone'),
                ('Waterford', 'Waterford'), ('Westmeath', 'Westmeath'), ('Wexford', 'Wexford'), ('Wicklow', 'Wicklow')
                ] 
    
    name = forms.CharField(label="Full Name", max_length=100, required=True)
    address1 = forms.CharField(label="Address Line 1", max_length=100, required=True)
    address2 = forms.CharField(label="Address Line 2", max_length=100, required=True)
    county = forms.ChoiceField(label="Count", choices=COUNTIES, required=True)
    town = forms.CharField(label="Town", max_length=50, required=True)
    eircode = forms.CharField(label="Eircode/ZIP", max_length=8, min_length=7, required=True)
