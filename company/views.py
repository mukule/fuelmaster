from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from users.models import *
from .models import *
from inventory.models import *
from django.contrib.auth.decorators import login_required


@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = CompanyForm()
    return render(request, 'company/create_company.html', {'form': form})


@login_required
def company_detail_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user_branch = request.user.branch
    branches = Branch.objects.filter(company=company)
    users = CustomUser.objects.filter(company=company)
    user_count = users.count()
    branch_count = branches.count()

    context = {
        'company': company,
        'branches': branches,
        'branch_count': branch_count,
        'users': users,
        'users_count': user_count
    }
    return render(request, 'company/company_detail.html', context)


@login_required
def create_branch(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.company = company
            branch.save()

            company.company_branches += 1
            company.save()

            return redirect('company:company_detail', pk=company_id)
    else:
        form = BranchForm()

    return render(request, 'company/create_branch.html', {'form': form, 'company': company})


@login_required
def branch_detail_view(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    categories = Category.objects.filter(branch=branch)
    context = {
        'branch': branch,
        'categories': categories
    }
    return render(request, 'company/branch_detail.html', context)
