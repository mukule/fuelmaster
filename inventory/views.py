from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import *
from company.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from PIL import Image
import requests
from io import BytesIO
import tempfile
from reportlab.lib.pagesizes import letter
from users.decorators import *


@login_required
@company
def create_category(request, branch_id):

    branch = Branch.objects.get(pk=branch_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            category = form.save(commit=False)

            category.branch = branch
            category.save()
            return redirect('company:branch_detail', branch_id=branch_id)
    else:
        form = CategoryForm()

    return render(request, 'inventory/create_category.html', {'form': form, 'branch': branch})


@login_required
@company
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('company:branch_detail', branch_id=category.branch.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/edit_category.html', {'form': form, 'category': category})


@login_required
@company
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    branch_pk = category.branch.pk
    category.delete()
    return redirect('company:branch_detail', branch_id=branch_pk)


@login_required
@company
def category_detail(request, category_id):

    category = get_object_or_404(Category, pk=category_id)

    user_branch = request.user.branch

    products = Product.objects.filter(category=category, branch=user_branch)

    return render(request, 'inventory/category_detail.html', {'category': category, 'products': products, 'branch': user_branch})


@login_required
@company
def create_product(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    user_branch = request.user.branch  # Assuming you have access to the user's branch

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():

            product = form.save(commit=False)
            product.category = category
            product.branch = user_branch
            product.save()
            return redirect('inventory:category_detail', category_id=category.pk)
    else:
        form = ProductForm()
    return render(request, 'inventory/create_product.html', {'form': form, 'category': category})


@login_required
@company
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:category_detail', category_id=product.category.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product})


@login_required
@company
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    category_pk = product.category.pk
    product.delete()
    return redirect('inventory:category_detail', category_id=category_pk)


@login_required
@company
def suppliers(request):
    user_company = request.user.company

    suppliers = Supplier.objects.filter(company=user_company)

    return render(request, 'inventory/suppliers.html', {'suppliers': suppliers})


@login_required
@company
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            user_company = request.user.company
            supplier.company = user_company
            supplier.save()
            messages.success(request, 'Supplier created successfully.')
            return redirect('inventory:suppliers')
        else:
            # If form is invalid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = SupplierForm()

    return render(request, 'inventory/create_supplier.html', {'form': form})


@login_required
@company
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('inventory:suppliers')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'inventory/edit_supplier.html', {'form': form, 'supplier': supplier})


@login_required
@company
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    supplier.delete()
    return redirect('inventory:suppliers')


@login_required
@company
def orders(request):
    user_branch = request.user.branch
    print("hello")

    orders = Order.objects.filter(branch=user_branch)
    print(orders)

    return render(request, 'inventory/orders.html', {'orders': orders})


@login_required
@company
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            last_order = Order.objects.last()
            if last_order and last_order.order_number:
                last_order_number = int(last_order.order_number)
            else:
                last_order_number = 0

            new_order_number = str(last_order_number + 1).zfill(4)

            form.instance.order_number = new_order_number
            user_branch = request.user.branch
            form.instance.branch = user_branch

            form.save()

            return redirect('inventory:orders')
    else:
        form = OrderForm()

    return render(request, 'inventory/create_order.html', {'form': form})


@login_required
@company
def edit_order(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('inventory:orders')
    else:
        form = OrderForm(instance=order)

    return render(request, 'inventory/edit_order.html', {'form': form, 'order': order})


@login_required
@company
def receivings(request):
    user_branch = request.user.branch

    orders = Order.objects.filter(branch=user_branch)

    return render(request, 'inventory/receivings.html', {'orders': orders})


@login_required
@company
def create_receiving(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    existing_receiving = Receiving.objects.filter(order=order).exists()

    if existing_receiving:
        messages.error(request, "This order has already been received.")
        return redirect('inventory:receivings')

    if request.method == 'POST':
        form = ReceivingForm(request.POST)
        if form.is_valid():
            receiving = form.save(commit=False)
            receiving.order = order
            receiving.received_by = request.user
            receiving.branch = request.user.branch
            receiving.save()

            # Update product quantity
            product = order.product
            product.quantity += receiving.quantity
            product.save()

            order.status = True
            order.save()

            # Create or update bill
            create_or_update_bill(receiving)

            return redirect('inventory:orders')
    else:
        form = ReceivingForm()

    return render(request, 'inventory/create_receiving.html', {'form': form, 'order': order})


@login_required
@company
def create_or_update_bill(receiving):

    bill, created = Bill.objects.get_or_create(order=receiving.order)

    bill.branch = receiving.branch
    bill.receiving = receiving

    bill.status = True

    total_amount = receiving.price * receiving.quantity
    bill.total_amount = total_amount

    bill.save()


@login_required
@company
def bills(request):
    user_branch = request.user.branch

    bills = Bill.objects.filter(branch=user_branch)

    return render(request, 'inventory/bills.html', {'bills': bills})


def generate_pdf(request, bill_id):
    # Retrieve the bill object based on the bill_id
    bill = Bill.objects.get(id=bill_id)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    # Uniform padding
    padding = 50

    # Fetch the logo image from the URL
    logo_url = "https://healthtoday.co.ke/wp-content/uploads/2023/03/cropped-Logo-232x77.png"
    response = requests.get(logo_url)
    logo_image = Image.open(io.BytesIO(response.content))

    # Add logo with uniform padding
    logo_width, logo_height = 100, 50
    logo_x = padding
    logo_y = p._pagesize[1] - padding
    p.drawInlineImage(logo_image, logo_x, logo_y - logo_height,
                      width=logo_width, height=logo_height)

    # Add supplier title and name below the logo
    supplier_title_y = logo_y - logo_height - 30
    supplier_name_y = supplier_title_y - 20
    p.setFont("Times-Bold", 12)
    p.drawString(logo_x, supplier_title_y, "Supplier:")
    p.setFont("Times-Roman", 12)
    p.drawString(logo_x, supplier_name_y, bill.order.supplier.name)

    # Add title with font Times-Roman Bold
    title_text = f"Invoice Number: {bill.branch.name}_{bill.order.order_number}"
    title_width = p.stringWidth(title_text, "Times-Bold", 12)
    title_x = p._pagesize[0] - title_width - padding
    title_y = logo_y - logo_height - 30
    p.setFont("Times-Bold", 12)
    p.drawString(title_x, title_y, title_text)

    # Add date aligned far right
    date_text = f"Date: {bill.receiving.received_on}"
    date_width = p.stringWidth(date_text, "Times-Roman", 12)
    date_x = p._pagesize[0] - date_width - padding
    date_y = title_y - 20
    p.drawString(date_x, date_y, date_text)

    # Define table headers
    headers = ["Product", "Quantity", "Unit", "Price", "Total"]
    table_y = date_y - 80
    table_width = p._pagesize[0] - 2 * padding
    cell_width = table_width / len(headers)

    # Define row height
    row_height = 20

    # Set font for header
    p.setFont("Times-Bold", 12)
    for i, header in enumerate(headers):
        p.drawString(padding + i * cell_width, table_y, header)

    # Add table content
    product = bill.order.product
    row_y = table_y - row_height
    p.setFont("Times-Roman", 12)
    p.drawString(padding, row_y, f"{product.name} - {product.product_code}")
    p.drawString(padding + cell_width, row_y, str(bill.receiving.quantity))
    p.drawString(padding + 2 * cell_width, row_y, product.unit)
    p.drawString(padding + 3 * cell_width, row_y, str(bill.receiving.price))
    # Convert Decimal to string for total
    total = str(bill.total_amount)
    p.drawString(padding + 4 * cell_width, row_y, total)

    # Add total sum
    total_sum_text = f"Total Sum: {total}"
    total_sum_x = p._pagesize[0] - \
        p.stringWidth(total_sum_text, "Times-Roman", 12) - padding
    total_sum_y = table_y - 6 * row_height - 10
    p.drawString(total_sum_x, total_sum_y, total_sum_text)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"invoice_bill_{bill.branch.name}_{bill.order.order_number}.pdf")


@login_required
@company
def receive_virtual_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_branch = request.user.branch  # Retrieve the branch of the logged-in user

    if request.method == 'POST':
        form = ReceiveVirtualForm(request.POST)
        if form.is_valid():
            receive_instance = form.save(commit=False)
            receive_instance.product = product
            receive_instance.branch = user_branch
            receive_instance.receive_by = request.user
            receive_instance.receiver_id = request.user.id
            receive_instance.save()

            # Update product quantity
            product.quantity += receive_instance.quantity
            product.save()

            return redirect('inventory:virtual_warehouse')
    else:
        form = ReceiveVirtualForm()

    return render(request, 'inventory/receive_virtual_product.html', {'form': form, 'branch': user_branch})


@login_required
@company
def issue_virtual_product(request, virtual_product_id):
    virtual_product = get_object_or_404(ReceiveVirtual, id=virtual_product_id)
    branch = request.user.branch

    # Check if the virtual product has already been issued
    if virtual_product.issued:
        return redirect('inventory:virtual_warehouse')

    if request.method == 'POST':
        form = IssueVirtualForm(request.POST)
        if form.is_valid():
            issue_instance = form.save(commit=False)
            issue_instance.product = virtual_product.product
            issue_instance.branch = request.user.branch
            issue_instance.issued_by = request.user

            # Check if the requested quantity is greater than available quantity
            if issue_instance.quantity <= virtual_product.quantity:
                issue_instance.save()

                virtual_product.product.quantity -= issue_instance.quantity
                virtual_product.product.save()

                virtual_product.issued = True
                virtual_product.save()

                return redirect('inventory:virtual_warehouse')
            else:
                form.add_error(
                    'quantity', 'Cannot issue more than available quantity.')
    else:
        # Set the initial quantity in the form
        initial_quantity = virtual_product.quantity
        form = IssueVirtualForm(initial={'quantity': initial_quantity})

    return render(request, 'inventory/issue_virtual_product.html', {'form': form, 'virtual_product': virtual_product, 'branch': branch})


@login_required
@company
def vproducts(request):
    user_branch = request.user.branch
    branch_id = user_branch.id

    products = Product.objects.filter(branch=user_branch)

    return render(request, 'inventory/vproducts.html', {'products': products, 'branch': user_branch})


@login_required
@company
def virtual_warehouse(request):
    user_branch = request.user.branch

    virtual_products = ReceiveVirtual.objects.filter(
        branch=user_branch).order_by('-receive_date')

    return render(request, 'inventory/virtual_warehouse.html', {'vproducts': virtual_products, 'branch': user_branch})


@login_required
@company
def transfers(request):
    user_branch = request.user.branch

    transfers = ProductTransfer.objects.filter(
        models.Q(branch=user_branch) | models.Q(to_branch=user_branch)
    ).order_by('-transfer_date')

    return render(request, 'inventory/transfers.html', {'transfers': transfers, 'branch': user_branch})


@login_required
@company
def create_product_transfer(request):
    user_branch = request.user.branch

    if request.method == "POST":
        form = ProductTransferForm(request.POST)
        if form.is_valid():
            to_branch = form.cleaned_data['to_branch']
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            if to_branch.active:
                # Check if the destination branch is the same as the user's branch
                if to_branch == user_branch:
                    form.add_error(
                        'to_branch', 'You cannot transfer to your own branch')
                    messages.error(request, 'Self Transfers not Allowed')
                else:
                    # Check if the quantity being transferred is not more than the available quantity
                    if quantity > product.quantity:
                        form.add_error(
                            'quantity', 'The quantity to transfer exceeds available stock')
                        messages.error(
                            request, 'The quantity to transfer exceeds available stock')
                    else:
                        # Create the transfer and update product quantity
                        transfer = ProductTransfer.objects.create(
                            branch=user_branch,
                            to_branch=to_branch,
                            product=product,
                            quantity=quantity,
                            transfer_by=request.user
                        )
                        # Update product quantity after the transfer
                        product.quantity -= quantity
                        product.save()
                        return redirect('inventory:transfers')
            else:
                # Destination branch is not active
                form.add_error('to_branch', 'Destination branch is not active')
                messages.error(request, 'Destination branch is not active')
    else:
        form = ProductTransferForm(initial={'branch': user_branch})

    # Filter only active branches for destination branch dropdown and exclude user's branch
    active_branches = Branch.objects.filter(
        active=True).exclude(pk=user_branch.pk)

    return render(
        request,
        'inventory/create_product_transfer.html',
        {'form': form, 'active_branches': active_branches, 'branch': user_branch}
    )


@login_required
@company
def receive_product_transfer(request, transfer_id):
    user_branch = request.user.branch

    # Get the product transfer object
    transfer = get_object_or_404(ProductTransfer, id=transfer_id)

    # Check if the user's branch is the destination branch of the transfer
    if user_branch != transfer.to_branch:
        messages.error(
            request, 'You are not authorized to receive this transfer.')
        return redirect('inventory:transfers')

    transfer.received = True
    transfer.received_by = request.user
    transfer.save()

    # Check if the product category exists for the branch
    category, created = Category.objects.get_or_create(
        name=transfer.product.category.name, branch=user_branch)

    # Get or create the product for the user's branch and category
    product, created = Product.objects.get_or_create(branch=user_branch, category=category, name=transfer.product.name, defaults={
        'product_code': transfer.product.product_code,
        'unit': transfer.product.unit,
        'price': transfer.product.price,
        'quantity': 0  # Set default quantity to 0 if the product is created
    }
    )

    # Update the product details
    product.product_code = transfer.product.product_code
    product.unit = transfer.product.unit
    product.price = transfer.product.price

    # Update the product quantity
    product.quantity += transfer.quantity
    product.save()

    messages.success(request, 'Product transfer received successfully.')
    return redirect('inventory:transfers')
