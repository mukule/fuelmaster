# forms.py
from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': '',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit', 'price', 'product_code']
        labels = {
            'name': '',
            'quantity': '',
            'unit': '',
            'price': '',
            'product_code': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit eg Litre'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price, Amount per unit'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Code'}),
        }


class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_supplied'].empty_label = '-- Select a Product --'

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email',
                  'phone_number', 'address', 'product_supplied']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'product_supplied': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '',
            'contact_person': '',
            'email': '',
            'phone_number': '',
            'address': '',
            'product_supplied': '',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'supplier']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'product': '',
            'quantity': '',
            'supplier': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = 'Select a Product'
        self.fields['supplier'].empty_label = 'Select a Supplier'


class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = ['quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        }
        labels = {
            'quantity': '',
            'price': '',
        }


class ReceiveVirtualForm(forms.ModelForm):
    class Meta:
        model = ReceiveVirtual
        fields = ['receive_from',
                  'receiver_id', 'quantity']
        labels = {
            'receive_from': '',
            'receiver_id': '',
            'quantity': '',

        }
        widgets = {
            'receive_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Received From'}),
            'receiver_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver ID'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),

        }


class IssueVirtualForm(forms.ModelForm):
    class Meta:
        model = IssueVirtual
        fields = ['issue_to',
                  'issued_to_id', 'quantity']
        labels = {
            'issue_to': '',
            'issued_to_id': '',
            'quantity': '',
        }
        widgets = {
            'issue_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issued To'}),
            'issued_to_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issued To ID'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }


class ProductTransferForm(forms.ModelForm):
    class Meta:
        model = ProductTransfer
        fields = ['to_branch', 'product', 'quantity']
        labels = {
            'to_branch': '',
            'product': '',
            'quantity': '',
        }
        widgets = {
            'to_branch': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_branch'].empty_label = 'Select a branch to Transfer to'
        self.fields['product'].empty_label = 'Select a product to Transfer'
