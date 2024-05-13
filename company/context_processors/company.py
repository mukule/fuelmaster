from company.models import *
from inventory.models import *


def branches_in_company(request):
    branches = []
    company_id = None
    if request.user.is_authenticated and request.user.company:
        branches = Branch.objects.filter(company=request.user.company)
        company_id = request.user.company.pk
    return {'branches': branches, 'company_id': company_id}


def warehouse_in_branch(request):
    branches = []
    company_id = None
    if request.user.is_authenticated and request.user.company:
        branches = Branch.objects.filter(company=request.user.company)
        company_id = request.user.company.pk
    return {'branches': branches, 'company_id': company_id}


def warehouse_in_branch(request):
    warehouses = []
    branches = []
    company_id = None
    if request.user.is_authenticated and request.user.company:
        branches = Branch.objects.filter(company=request.user.company)
        company_id = request.user.company.pk
        for branch in branches:
            warehouses.extend(Warehouse.objects.filter(branch=branch))
    return {'warehouses': warehouses, 'branches': branches, 'company_id': company_id}
