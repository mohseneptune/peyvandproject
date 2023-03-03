from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, get_user_model
from account.forms import RegisterForm, OTPForm, LoginForm, PhoneChangeForm, ProfileChangeForm, KhosousiaatFrom, EntezaaraatFrom, PartnerSearchForm
from random import randint
from core.otp import send_opt
from django.contrib import messages
from account.models import Khosousiaat, Entezaaraat
from django.forms.models import model_to_dict


User = get_user_model()


def register_view(request):
    template_name = "account/register.html"
    template_title = "ثبت نام"
    form = RegisterForm

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            register_form_data = form.cleaned_data
            otp = randint(100000, 999999)
            request.session["register_form_data"] = register_form_data
            request.session["otp"] = otp
            send_opt(register_form_data["phone"], otp)
            
            return redirect("account:register_verify")

    context = {
        "template_title": template_title,
        "form": form,
    }

    return render(request, template_name, context)


def register_verify_view(request):
    template_name = "account/verify.html"
    template_title = "تایید شماره موبایل"
    form = OTPForm
    form_error = None

    if ("register_form_data" not in request.session) or ("otp" not in request.session):
        return redirect("account:register")

    phone = request.session["register_form_data"]["phone"]
    otp = request.session.get("otp")

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data["otp"]
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
        "template_title": template_title,
        "form": form,
        "form_error": form_error,
        "phone": phone,
        "otp": otp
    }

    return render(request, template_name, context)


def login_view(request):
    template_name = "account/login.html"
    template_title = "ورود"
    form = LoginForm

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = randint(100000, 999999)
            request.session["phone"] = phone
            request.session["otp"] = otp
            send_opt(phone, otp)
            return redirect("account:login_verify")

    context = {
        "template_title": template_title,
        "form": form,
    }
    return render(request, template_name, context)


def login_verify_view(request):
    template_name = "account/verify.html"
    template_title = "تایید شماره موبایل"
    form = OTPForm
    form_error = None

    if ("phone" not in request.session) or ("otp" not in request.session):
        return redirect("account:login")

    phone = request.session.get("phone")
    otp = request.session.get("otp")

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data["otp"]
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
        "template_title": template_title,
        "form": form,
        "form_error": form_error,
        "phone": phone,
        "otp": otp
    }
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return redirect("account:login")


def profile_view(request):
    template_name = "account/profile.html"
    template_title = "حساب کاربری"

    try:
        khosousiaat = request.user.khosousiaat
    except:
        khosousiaat = Khosousiaat.objects.create(user=request.user)

    try:
        entezaaraat = request.user.entezaaraat
    except:
        entezaaraat = Entezaaraat.objects.create(user=request.user)

    context = {"template_title": template_title, "khosousiaat": khosousiaat, "entezaaraat": entezaaraat}
    return render(request, template_name, context)


def phone_change_view(request):
    template_name = "account/phone_change.html"
    template_title = "ویرایش شماره موبایل"

    if request.method == "POST":
        form = PhoneChangeForm(data=request.POST, instance=request.user)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = randint(100000, 999999)
            request.session["phone"] = phone
            request.session["otp"] = otp
            send_opt(phone, otp)
            messages.success(request, "کد تایید به شماره موبایل شما ارسال شد")
            return redirect("account:phone_change_verify")
        else:
            messages.error(request, "خطا در ثبت اطلاعات. لطفا دوباره تلاش کنید.")

    else:
        form = PhoneChangeForm(instance=request.user)

    context = {"template_title": template_title, "form": form}
    return render(request, template_name, context)


def phone_change_verify_view(request):
    template_name = "account/phone_change_verify.html"
    template_title = "تایید شماره موبایل"

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            form_otp = form.cleaned_data["otp"]
            phone = request.session.get("phone")
            otp = request.session.get("otp")

            if form_otp == otp:
                user = request.user
                user.phone = phone
                user.save()
                messages.success(request, "شماره موبایل شما با موفقیت ویراش شد")
                return redirect('account:profile')
            else:
                messages.error(request, "کد وارد شده اشتباه است. دوباره تلاش کنید.")

        else:
            messages.error(request, "کد وارد شده اشتباه است. دوباره تلاش کنید.")
    else:
        form = OTPForm()

    context = {"template_title": template_title, "form": form}
    return render(request, template_name, context)


def profile_change_view(request):
    template_name = "account/phone_change_verify.html"
    template_title = "تایید شماره موبایل"

    if request.method == 'POST':
        form = ProfileChangeForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "حساب کاربری شما با موفقیت ویرایش شد")
            return redirect("account:profile")
        
        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = ProfileChangeForm(instance=request.user)
    
    context = {"template_title": template_title, "form": form}
    return render(request, template_name, context)


def khosousiaat_change_view(request):
    template_name = "account/khosousiaat_change.html"
    template_title = "ویرایش خصوصیات"

    khosousiaat, created = Khosousiaat.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = KhosousiaatFrom(instance=khosousiaat, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "خصوصیات شما با موفقیت ویرایش شد")
            return redirect("account:profile")
        
        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = KhosousiaatFrom(instance=khosousiaat)
    
    context = {"template_title": template_title, "form": form}
    return render(request, template_name, context)


def entezaaraat_change_view(request):
    template_name = "account/entezaaraat_change.html"
    template_title = "ویرایش خصوصیات"

    entezaaraat, created = Entezaaraat.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EntezaaraatFrom(instance=entezaaraat, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "انتظارات شما با موفقیت ویرایش شد")
            return redirect("account:profile")
        
        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = EntezaaraatFrom(instance=entezaaraat)
    
    context = {"template_title": template_title, "form": form}
    return render(request, template_name, context)


def partner_search_view(request):
    template_name = "account/partner_search.html"
    template_title = "جستجوی همسان"
    user = request.user
    entezaaraat = Entezaaraat.objects.get(user=user)

    if user.gender == "1":
        users = User.objects.exclude(pk=request.user.pk).filter(gender="2")
    else:
        users = User.objects.exclude(pk=request.user.pk).filter(gender="1")

    partners = Khosousiaat.objects.filter(user__in=users)

    # partners = partners.filter(tavallod__in=entezaaraat.tavallod_range())
    # partners = partners.filter(qad__in=entezaaraat.qad_range())
    # partners = partners.filter(vazn__in=entezaaraat.vazn_range())    

    # if entezaaraat.zibaayi != '0' and entezaaraat.zibaayi != None:
    #     partners = partners.filter(zibaayi=entezaaraat.zibaayi)

    # if entezaaraat.ostaane_tavallod != '0' and entezaaraat.ostaane_tavallod != None:
    #     partners = partners.filter(ostaane_tavallod=entezaaraat.ostaane_tavallod)
    
    # if entezaaraat.ostaane_sokounat != '0' and entezaaraat.ostaane_sokounat != None:
    #     partners = partners.filter(ostaane_sokounat=entezaaraat.ostaane_sokounat)

    # if entezaaraat.shahre_sokounat != '0' and entezaaraat.shahre_sokounat != None:
    #     partners = partners.filter(shahre_sokounat=entezaaraat.shahre_sokounat)

    # if entezaaraat.ehsaasaat != '0' and entezaaraat.ehsaasaat != None:
    #     partners = partners.filter(ehsaasaat=entezaaraat.ehsaasaat)

    # if entezaaraat.ertebaataat != '0' and entezaaraat.ertebaataat != None:
    #     partners = partners.filter(ertebaataat=entezaaraat.ertebaataat)

    # if entezaaraat.jensi != '0' and entezaaraat.jensi != None:
    #     partners = partners.filter(jensi=entezaaraat.jensi)

    # if entezaaraat.salaamat != '0' and entezaaraat.salaamat != None:
    #     partners = partners.filter(salaamat=entezaaraat.salaamat)

    if entezaaraat.tahsil != '0' and entezaaraat.tahsil != None:
        partners = partners.filter(tahsil=entezaaraat.tahsil)
    
    if entezaaraat.qowmiat != '0' and entezaaraat.qowmiat != None:
        partners = partners.filter(qowmiat=entezaaraat.qowmiat)

    if entezaaraat.shoql != '0' and entezaaraat.shoql != None:
        partners = partners.filter(shoql=entezaaraat.shoql)

    if entezaaraat.din != '0' and entezaaraat.din != None:
        partners = partners.filter(din=entezaaraat.din)    

    context = {
        'template_title': template_title,
        'partners': partners
    }

    return render(request, template_name, context)



def user_detail_view(request, pk):
    template_name = "account/user_detail.html"
    template_title = "مشخصات کاربر"

    detail = get_object_or_404(User, pk=pk)
    khosousiaat = detail.khosousiaat
    entezaaraat = detail.entezaaraat

    context = {
        'template_title': template_title,
        'detail': detail,
        'khosousiaat': khosousiaat,
        'entezaaraat': entezaaraat,
    }

    return render(request, template_name, context)
