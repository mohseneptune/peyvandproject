from django.shortcuts import render, redirect
from django.contrib.auth import logout


def register_view(request):
    template_name = 'account/register.html'
    template_title = 'ثبت نام'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)



def login_view(request):
    template_name = 'account/login.html'
    template_title = 'ورود'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)


def profile_view(request):
    template_name = 'account/profile.html'
    template_title = 'حساب کاربری'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)


def profile_change_view(request):
    template_name = 'account/profile_change.html'
    template_title = 'ویرایش حساب کاربری'


    context = {
        'template_title': template_title
    }
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect('account:login')