# forms.py
from django import forms
from .models import *
import pycountry


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '-- Select product type --'
        self.fields['sales_account'].empty_label = '-- Select sales account --'
        self.fields['purchases_account'].empty_label = '-- Select purchases account --'
        self.fields['warehouse'].empty_label = '-- Select Warehouse --'

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit', 'product_code', 'category', 'description', 'sales_account',
                  'selling_price', 'buying_price', 'purchases_account', 'warehouse', 'image']
        labels = {
            'name': '',
            'quantity': '',
            'unit': '',
            'product_code': '',
            'category': 'Category',
            'description': 'Description',
            'sales_account': 'Sales Account',
            'selling_price': 'Selling Price',
            'buying_price': 'Buying Price',
            'purchases_account': 'Purchases Account',
            'warehouse': 'Warehouse',
            'image': 'Image',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit eg Litre, pcs'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Code'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'sales_account': forms.Select(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'buying_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'purchases_account': forms.Select(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'id': 'image-uploadify'}),
        }


class CompositeProductForm(forms.ModelForm):
    class Meta:
        model = CompositeProduct
        fields = ['name', 'description', 'components']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'components': 'Components',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the composite product'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter the description of the composite product'}),
            'components': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        # Make components required
        required = {
            'components': True,
        }


class AdjustmentForm(forms.ModelForm):
    class Meta:
        model = Adjustment
        fields = ['ref_number', 'reason', 'branch', 'warehouse',
                  'description', 'product', 'quantity']
        labels = {
            'ref_number': 'Reference Number',
            'reason': 'Reason',
            'branch': 'Branch',
            'warehouse': 'Warehouse',
            'description': 'Description',
            'product': 'Product',
            'quantity': 'Quantity',

        }
        widgets = {
            'ref_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].empty_label = '-- Select Reason --'
        self.fields['branch'].empty_label = '-- Select Branch --'
        self.fields['warehouse'].empty_label = '-- Select Warehouse --'


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


class ReasonForm(forms.ModelForm):
    class Meta:
        model = AdjustmentReason
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adjustment Reason'}),
        }
        labels = {
            'name': '',
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


class WarehouseForm(forms.ModelForm):
    country_choices = [(country.alpha_2, country.name)
                       for country in pycountry.countries]

    # Add a country field to the form with the choices populated from pycountry
    country = forms.ChoiceField(
        choices=country_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].widget.attrs.update({'class': 'form-control'})
        self.fields['branch'].choices = [
            ('', 'Choose Branch')] + list(self.fields['branch'].choices)

    class Meta:
        model = Warehouse
        fields = ['name', 'country', 'county',
                  'city', 'phone', 'email', 'branch']
        labels = {
            'name': 'Name',
            'county': 'County',
            'city': 'City',
            'phone': 'Phone',
            'email': 'Email',
            'country': 'Country',
            'branch': 'Branch',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warehouse Name'}),
            'county': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'County'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
        }


class SalesAccountForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Select a branch",
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = SalesAccount
        fields = ['name', 'branch']
        labels = {
            'name': 'Name',
            'branch': 'Branch',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sales account name'}),
        }


class PurchasesAccountForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Select a branch",
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = PurchasesAccount
        fields = ['name', 'branch']
        labels = {
            'name': 'Name',
            'branch': 'Branch',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter purchases account name'}),
        }


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['transfer_order', 'reason', 'source_warehouse',
                  'destination_warehouse', 'product', 'quantity']
        labels = {
            'transfer_order': 'Transfer Order',
            'reason': 'Reason',
            'source_warehouse': 'Source Warehouse',
            'destination_warehouse': 'Destination Warehouse',
            'product': 'Product',
            'quantity': 'Quantity',
        }
        widgets = {
            'transfer_order': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
            'source_warehouse': forms.Select(attrs={'class': 'form-control'}),
            'destination_warehouse': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_warehouse'].empty_label = '-- Select Source Warehouse --'
        self.fields['destination_warehouse'].empty_label = '-- Select Destination Warehouse --'
        self.fields['product'].empty_label = '-- Select Product --'
