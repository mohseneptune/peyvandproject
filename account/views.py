from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, get_user_model
from account.forms import RegisterForm, OTPForm, LoginForm
from random import randint
from core.otp import send_opt


User = get_user_model()


def register_view(request):
    template_name = 'account/register.html'
    template_title = 'ثبت نام'
    form = RegisterForm

    if request.POST:
        form = form(request.POST)
        
        if form.is_valid():
            register_form_data = form.cleaned_data
            otp = randint(100000, 999999)
            request.session["register_form_data"] = register_form_data
            request.session["otp"] = otp
            send_opt(register_form_data["phone"], otp)
            return redirect("account:register_verify")

    context = {
        'template_title': template_title,
        'form': form,
    }

    return render(request, template_name, context)


def register_verify_view(request):
    template_name = 'account/verify.html'
    template_title = 'تایید شماره موبایل'
    form = OTPForm
    form_error = None

    if ("register_form_data" not in request.session) or ("otp" not in request.session):
        return redirect("account:register")

    phone = request.session['register_form_data']['phone']

    if request.method == 'POST':
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data['otp']
            register_form_data = request.session.get("register_form_data")
            otp = request.session.get("otp")

            if form_otp == otp:
                user = User.objects.create(**register_form_data)
                login(request, user, "core.backends.PasswordlessAuthBackend")
                request.session.pop("register_form_data")
                request.session.pop("otp")
                return redirect("account:profile")
            else:
                form_error = "کد وارد شده اشتباه است"

    context = {
        'template_title': template_title,
        'form': form,
        'form_error': form_error,
        'phone': phone
    }
    
    return render(request, template_name, context)


def login_view(request):
    template_name = 'account/login.html'
    template_title = 'ورود'
    form = LoginForm

    if request.method == 'POST':
        form = form(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = randint(100000, 999999)
            request.session["phone"] = phone
            request.session["otp"] = otp
            send_opt(phone, otp)
            return redirect('account:login_verify')

    context = {
        'template_title': template_title,
        'form': form,
    }
    return render(request, template_name, context)


def login_verify_view(request):
    template_name = 'account/verify.html'
    template_title = 'تایید شماره موبایل'
    form = OTPForm
    form_error = None

    if ("phone" not in request.session) or ("otp" not in request.session):
        return redirect("account:login")

    phone = request.session.get("phone")

    if request.method == 'POST':
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data['otp']
            phone = request.session.get("phone")
            otp = request.session.get("otp")

            if form_otp == otp:
                user = get_object_or_404(User, phone=phone)
                login(request, user, "core.backends.PasswordlessAuthBackend")
                request.session.pop("phone")
                request.session.pop("otp")
                return redirect("account:profile")
            else:
                form_error = "کد وارد شده اشتباه است"

    context = {
        'template_title': template_title,
        'form': form,
        'form_error': form_error,
        'phone': phone
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