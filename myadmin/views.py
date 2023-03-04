from django.shortcuts import render, get_object_or_404, redirect
from account.models import Relation, Khosousiaat, Entezaaraat
from django.contrib.auth import get_user_model


User = get_user_model()


def dashboard_view(request):
    template_name = "myadmin/dashboard.html"
    template_title = "پنل مدیریت"
    
    context = {
        'template_title': template_title,
    }

    return render(request, template_name, context)



def requests_list_view(request):
    template_name = "myadmin/requests_list.html"
    template_title = "لیست درخواست ها"

    relations = Relation.objects.filter(status='2')
    
    context = {
        'template_title': template_title,
        'relations': relations
    }

    return render(request, template_name, context)


def user_detail_view(request, pk):
    template_name = "myadmin/user_detail.html"
    template_title = "مشخصات کاربر"

    account = get_object_or_404(User, pk=pk)

    khosousiaat = get_object_or_404(Khosousiaat, user=account)
    entezaaraat = get_object_or_404(Entezaaraat, user=account)
    
    print(khosousiaat)

    context = {
        'template_title': template_title,
        'account': account,
        'khosousiaat': khosousiaat,
        'entezaaraat': entezaaraat
    }

    return render(request, template_name, context)
