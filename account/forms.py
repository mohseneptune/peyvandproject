from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator



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
        regex=r"^09\d{9}$", message="شماره موبایل اشتباه میباشد")
    
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
