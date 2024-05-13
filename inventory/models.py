from django.db import models
from company.models import *
from users.models import *
from django.utils import timezone


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='warehouses'
    )

    def __str__(self):
        return self.name


class SalesAccount(models.Model):
    name = models.CharField(max_length=100)

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='sales_accounts', null=True, blank=True)

    def __str__(self):
        return self.name


class PurchasesAccount(models.Model):
    name = models.CharField(max_length=100)

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='purchases_accounts', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    product_code = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sales_account = models.ForeignKey(
        SalesAccount, on_delete=models.SET_NULL, null=True, blank=True)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    purchases_account = models.ForeignKey(
        PurchasesAccount, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='product_images',
                              default='default_product_image.jpg', null=True, blank=True)

    def __str__(self):
        return self.name


class CompositeProduct(models.Model):
    name = models.CharField(max_length=100)
    components = models.ManyToManyField(
        'Product', related_name='composite_of')
    description = models.TextField(null=True, blank=True)
    buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductTransfer(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True,)
    to_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='transfers_to'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='transfers'
    )
    quantity = models.FloatField()
    transfer_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='transfers_made'
    )
    received_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='transfers_received'
    )
    received = models.BooleanField(default=False)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.from_branch} to {self.to_branch} for {self.product} ({self.quantity})"


class ReceiveVirtual(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='received_virtual_product')
    receive_from = models.CharField(max_length=100)
    receive_date = models.DateField(auto_now_add=True)
    receive_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver_id = models.IntegerField()  # Assuming receiver_id is an integer
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    issued = models.BooleanField(default=False)

    def __str__(self):
        return f"Received Virtual: {self.receive_date} - {self.branch}"


class IssueVirtual(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='issued_virtual_product')
    issue_to = models.CharField(max_length=100)
    issue_date = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issued_to_id = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Issue Virtual: {self.issue_date} - {self.branch}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    product_supplied = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='suppliers', blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='suppliers', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.order_number


class Receiving(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    received_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    received_on = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Receiving for Order #{self.order_number}"


class Bill(models.Model):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receiving = models.ForeignKey(
        Receiving, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Bill for Order #{self.order.order_number}"


class AdjustmentReason(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='adjustmentReason', null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Adjustment(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='adjustments', null=True, blank=True)
    ref_number = models.CharField(max_length=100)
    reason = models.ForeignKey(AdjustmentReason, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    adjusted_quantity = models.FloatField(null=True, blank=True)
    adjusted_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.ref_number


class Transfer(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='transfers', null=True, blank=True)
    transfer_order = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    reason = models.CharField(max_length=255)
    source_warehouse = models.ForeignKey(
        Warehouse, related_name='source_transfers', on_delete=models.CASCADE)
    destination_warehouse = models.ForeignKey(
        Warehouse, related_name='destination_transfers', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    transfer_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.transfer_order
