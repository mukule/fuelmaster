from inventory.models import SalesAccount, PurchasesAccount


def sales_accounts_processor(request):
    sales_accounts = SalesAccount.objects.all()
    return {'sales_accounts': sales_accounts}


def purchases_accounts_processor(request):
    purchases_accounts = PurchasesAccount.objects.all()
    return {'purchases_accounts': purchases_accounts}
