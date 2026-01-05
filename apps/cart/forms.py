from django import forms
from apps.products.models import Product
from apps.cart.models import Cart
from unfold.widgets import UnfoldAdminMultipleAutocompleteWidget
from django.contrib.admin.widgets import FilteredSelectMultiple

class CartProductForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset = Product.objects.all(),
        required=False,
        widget = FilteredSelectMultiple(verbose_name='Menu Items', is_stacked=False)
    )