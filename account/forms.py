from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from account.models import Khosousiaat, Entezaaraat


User = get_user_model()


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("phone", "first_name", "last_name", "gender", "register_for")

        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "register_for": forms.Select(attrs={"class": "form-select"}),
        }


class OTPForm(forms.Form):
    otp = forms.CharField(
        label="کد تایید",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def clean_otp(self):
        otp = str(self.cleaned_data.get("otp"))
        if len(otp) == 6 and otp.isdigit():
            return int(otp)
        raise forms.ValidationError("کد وارد شده اشتباه است")


class LoginForm(forms.Form):
    PHONE_REGEX = RegexValidator(
        regex=r"^09\d{9}$", message="شماره موبایل اشتباه میباشد"
    )

    phone = forms.CharField(
        label="شماره موبایل",
        validators=[PHONE_REGEX],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        phone = self.cleaned_data.get("phone")
        if User.objects.filter(phone=phone).exists():
            return self.cleaned_data
        raise forms.ValidationError("این شماره موبایل در سیستم ثبت نشده است")


class PhoneChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("phone",)

        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("این شماره تماس قبلا در سیستم ثبت شده است")
        return phone


class ProfileChangeForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "gender", "register_for")

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "register_for": forms.Select(attrs={"class": "form-select"}),
        }

class KhosousiaatFrom(forms.ModelForm):

    class Meta:
        model = Khosousiaat
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(KhosousiaatFrom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.widget_type == 'select':
                visible.field.widget.attrs['class'] = 'form-select'
            else: visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.label



class EntezaaraatFrom(forms.ModelForm):

    class Meta:
        model = Entezaaraat
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(EntezaaraatFrom, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.widget_type == 'select':
                visible.field.widget.attrs['class'] = 'form-select'
            else: visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.label



class PartnerSearchForm(forms.Form):

    qad = forms.BooleanField(label='قد', required=False)
    vazn = forms.BooleanField(label='وزن', required=False)
    tahsil = forms.BooleanField(label='تحصیلات', required=False)
    tavallod = forms.BooleanField(label='سال تولد', required=False)
    zibaayi = forms.BooleanField(label='زیبایی', required=False)
    qowmiat = forms.BooleanField(label='قومیت', required=False)
    shoql = forms.BooleanField(label='شغل', required=False)
    shahre_sokounat = forms.BooleanField(label='شهر محل سکونت', required=False)
    ezdevaaj = forms.BooleanField(label='سابقه ازدواج', required=False)