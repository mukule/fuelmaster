from django.shortcuts import render, redirect
from company.models import *
from users.models import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = request.user
    if user.is_authenticated and user.access_level in [1, 2]:
        if user.company:
            return redirect('company:company_detail', pk=user.company.pk)

    company_count = Company.objects.count()
    branch_count = Branch.objects.count()
    users = CustomUser.objects.count()
    admin_user_count = CustomUser.objects.exclude(access_level=4).count()

    companies = Company.objects.all()

    context = {
        'company_count': company_count,
        'branch_count': branch_count,
        'admin_count': admin_user_count,
        'companies': companies,
        'users': users
    }
    return render(request, 'main/index.html', context)


@login_required
def branch(request):
    user = request.user
    if user.branch:
        branch_id = user.branch.pk
        return redirect('company:branch_detail', branch_id=branch_id)
    else:
        return redirect('main:index')
