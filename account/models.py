from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from account.choices import *


class UserManager(BaseUserManager):

    def create_superuser(self, phone, password, **other_fields):
        if not password:
            raise ValueError("رمز عبور اجباری میباشد")
        user = self.create_user(phone, password, **other_fields)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_user(self, phone, password, **other_fields):

        if not phone:
            raise ValueError("شماره موبایل اجباری میباشد")

        if password is not None:
            user = self.model(phone=phone, **other_fields)
            user.set_password(password)
            user.save()
        else:
            user = self.model(phone=phone, **other_fields)
            user.set_unusable_password()
            user.save()

        return user


class User(AbstractBaseUser):
    PHONE_REGEX = RegexValidator(
        regex=r"^09\d{9}$", message="شماره موبایل اشتباه میباشد")
    phone = models.CharField(
        "شماره موبایل", max_length=11, unique=True, validators=[PHONE_REGEX])
    first_name = models.CharField("نام", max_length=100)
    last_name = models.CharField("نام خانوادگی", max_length=100)
    gender = models.CharField("جنسیت", max_length=1,
                              choices=GENDER_CHOICES, default="1")
    register_for = models.CharField(
        "ثبت نام برای", max_length=1, choices=REGISTER_FOR_CHOICES, default="1")

    is_active = models.BooleanField("فعال", default=True)
    is_superuser = models.BooleanField("ابرکاربر", default=False)  # superuser
    is_admin = models.BooleanField("رابط", default=False)  # connector
    is_staff = models.BooleanField("کارشناس", default=False)  # expert

    joined_date = models.DateTimeField("تاریخ ثبت نام", auto_now_add=True)
    last_login = models.DateTimeField("تاریخ آخرین ورود", auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.is_superuser:
            return 'ادمین'
        if self.is_admin:
            return 'رابط'
        if self.is_staff:
            return 'کارشناس'
        return 'user'


    class Meta:
        db_table = "users"
        managed = True
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"



class Khosousiaat(models.Model):
    user = models.OneToOneField(User, verbose_name="کاربر", on_delete=models.CASCADE)
    
    tavallod = models.CharField("سال تولد", max_length=4, choices=TAVALLOD_CHOICES, null=True, blank=True)
    qad = models.CharField("قد", max_length=3, choices=QAD_CHOICES, null=True, blank=True)
    vazn = models.CharField("وزن", max_length=3, choices=VAZN_CHOICES, null=True, blank=True)
    tahsil = models.CharField("تحصیلات", max_length=1, choices=TAHSIL_CHOICES[1:], null=True, blank=True)
    rang = models.CharField("رنگ پوست", max_length=1, choices=RANG_CHOICES[1:], null=True, blank=True)
    zibaayi = models.CharField("میزان زیبایی", max_length=1, choices=ZIBAAYI_CHOICES[1:], null=True, blank=True)
    qowmiat = models.CharField("قومیت", max_length=1, choices=QOWMIAT_CHOICES[1:], null=True, blank=True)
    shoql = models.CharField("وضعیت اشتغال", max_length=1, choices=SHOQL_CHOICES[1:], null=True, blank=True)
    ostaane_tavallod = models.CharField("استان محل تولد", max_length=2, choices=OSTAANHAA_CHOICES[1:], null=True, blank=True)
    ostaane_sokounat = models.CharField("استان محل سکونت", max_length=2, choices=OSTAANHAA_CHOICES[1:], null=True, blank=True)
    shahre_sokounat = models.CharField("شهر محل سکونت", max_length=150, null=True, blank=True)

    ezdevaaj = models.CharField("سابقه ازدواج", max_length=1, choices=EZDEVAAJ_CHOICES[1:], null=True, blank=True)
    kharide_khodro = models.CharField("توانایی خرید خودرو", max_length=1, choices=KHARIDE_KHODRO_CHOICES[1:], null=True, blank=True)
    ehsaasaat = models.CharField("وضعیت احساسی", max_length=1, choices=EHSAASAAT_CHOICES[1:], null=True, blank=True)
    ertebaataat = models.CharField("راتباطات اجتماعی", max_length=1, choices=ERTEBAATAAT_CHOICES[1:], null=True, blank=True)
    jensi = models.CharField("امور جنسی", max_length=1, choices=JENSI_CHOICES[1:], null=True, blank=True)
    khaanevaadegi = models.CharField("امور خانوادگی", max_length=1, choices=KHAANEVAADEGI_CHOICES[1:], null=True, blank=True)
    salaamat = models.CharField("سلامت جسمی و روانی", max_length=1, choices=SALAAMAT_CHOICES[1:], null=True, blank=True)

    din = models.CharField("دین یا مذهب", max_length=1, choices=DIN_CHOICES[1:], null=True, blank=True)
    eteqaadaat = models.CharField("اعتقادات مذهبی", max_length=1, choices=ETEQAADAAT_CHOICES[1:], null=True, blank=True)
    amal_be_ahkaam = models.CharField("میزان عمل به احکام دینی", max_length=1, choices=AMAL_BE_AHKAAM_CHOICES[1:], null=True, blank=True)
    talabeh = models.BooleanField("طلبه", null=True, blank=True)
    seyyed = models.BooleanField("سید", null=True, blank=True)
    shekrat_dar_maraasemaat = models.CharField("شرکت در مراسم مذهبی و اجتماعی", max_length=1, choices=SHERKAT_DAR_MARAASEMAAT_CHOICES[1:], null=True, blank=True)
    pushesh = models.CharField("پوشش و لباس", max_length=1, choices=POUSHESH_CHOICES[1:], null=True, blank=True)

    tahsil_pedar = models.CharField("تحصیلات پدر", max_length=1, choices=TAHSIL_CHOICES[1:], null=True, blank=True)
    shoql_pedar = models.CharField("شغل پدر", max_length=1, choices=SHOQLE_VAALEDEIN_CHOICES[1:], null=True, blank=True)
    tahsil_maadar = models.CharField("تحصیلات مادر", max_length=1, choices=TAHSIL_CHOICES[1:], null=True, blank=True)
    shoql_maadar = models.CharField("شغل مادر", max_length=1, choices=SHOQLE_VAALEDEIN_CHOICES[1:], null=True, blank=True)
    kharide_khodro_pedari = models.CharField("توانایی خرید خودرو در خانواده پدری", max_length=1, choices=KHARIDE_KHODRO_CHOICES[1:], null=True, blank=True)
    
    tozihaat = models.TextField("دیگر توضیحات", null=True, blank=True)
    

    def __str__(self):
        return self.user.phone

    class Meta:
        db_table = "khosousiaat"
        managed = True
        verbose_name = "خصوصیات کاربر"
        verbose_name_plural = "خصوصیات کاربران"



class Entezaaraat(models.Model):
    user = models.OneToOneField(User, verbose_name="کاربر", on_delete=models.CASCADE)
    
    tavallod_from = models.CharField("سال تولد از", max_length=4, choices=TAVALLOD_CHOICES, null=True, blank=True)
    tavallod_to = models.CharField("سال تولد تا", max_length=4, choices=TAVALLOD_CHOICES, null=True, blank=True)
    qad_from = models.CharField("قد از", max_length=3, choices=QAD_CHOICES, null=True, blank=True)
    qad_to = models.CharField("قد تا", max_length=3, choices=QAD_CHOICES, null=True, blank=True)
    vazn_from = models.CharField("وزن از", max_length=3, choices=VAZN_CHOICES, null=True, blank=True)
    vazn_to = models.CharField("وزن تا", max_length=3, choices=VAZN_CHOICES, null=True, blank=True)
    tahsil = models.CharField("تحصیلات", max_length=1, choices=TAHSIL_CHOICES, null=True, blank=True)
    rang = models.CharField("رنگ پوست", max_length=1, choices=RANG_CHOICES, null=True, blank=True)
    zibaayi = models.CharField("میزان زیبایی", max_length=1, choices=ZIBAAYI_CHOICES, null=True, blank=True)
    qowmiat = models.CharField("قومیت", max_length=1, choices=QOWMIAT_CHOICES, null=True, blank=True)
    shoql = models.CharField("وضعیت اشتغال", max_length=1, choices=SHOQL_CHOICES, null=True, blank=True)
    ostaane_tavallod = models.CharField("استان محل تولد", max_length=2, choices=OSTAANHAA_CHOICES, null=True, blank=True)
    ostaane_sokounat = models.CharField("استان محل سکونت", max_length=2, choices=OSTAANHAA_CHOICES, null=True, blank=True)
    shahre_sokounat = models.CharField("شهر محل سکونت", max_length=150, null=True, blank=True)

    ezdevaaj = models.CharField("سابقه ازدواج", max_length=1, choices=EZDEVAAJ_CHOICES, null=True, blank=True)
    kharide_khodro = models.CharField("توانایی خرید خودرو", max_length=1, choices=KHARIDE_KHODRO_CHOICES, null=True, blank=True)
    ehsaasaat = models.CharField("وضعیت احساسی", max_length=1, choices=EHSAASAAT_CHOICES, null=True, blank=True)
    ertebaataat = models.CharField("راتباطات اجتماعی", max_length=1, choices=ERTEBAATAAT_CHOICES, null=True, blank=True)
    jensi = models.CharField("امور جنسی", max_length=1, choices=JENSI_CHOICES, null=True, blank=True)
    khaanevaadegi = models.CharField("امور خانوادگی", max_length=1, choices=KHAANEVAADEGI_CHOICES, null=True, blank=True)
    salaamat = models.CharField("سلامت جسمی و روانی", max_length=1, choices=SALAAMAT_CHOICES, null=True, blank=True)

    din = models.CharField("دین یا مذهب", max_length=1, choices=DIN_CHOICES, null=True, blank=True)
    eteqaadaat = models.CharField("اعتقادات مذهبی", max_length=1, choices=ETEQAADAAT_CHOICES, null=True, blank=True)
    amal_be_ahkaam = models.CharField("میزان عمل به احکام دینی", max_length=1, choices=AMAL_BE_AHKAAM_CHOICES, null=True, blank=True)
    talabeh = models.CharField("طلبه", max_length=1, choices=TALABEH_CHOICES, null=True, blank=True)
    seyyed = models.CharField("سید", max_length=1, choices=SEYYED_CHOICES, null=True, blank=True)
    shekrat_dar_maraasemaat = models.CharField("شرکت در مراسم مذهبی و اجتماعی", max_length=1, choices=SHERKAT_DAR_MARAASEMAAT_CHOICES, null=True, blank=True)
    pushesh = models.CharField("پوشش و لباس", max_length=1, choices=POUSHESH_CHOICES, null=True, blank=True)

    tahsil_pedar = models.CharField("تحصیلات پدر", max_length=1, choices=TAHSIL_CHOICES, null=True, blank=True)
    shoql_pedar = models.CharField("شغل پدر", max_length=1, choices=SHOQLE_VAALEDEIN_CHOICES, null=True, blank=True)
    tahsil_maadar = models.CharField("تحصیلات مادر", max_length=1, choices=TAHSIL_CHOICES, null=True, blank=True)
    shoql_maadar = models.CharField("شغل مادر", max_length=1, choices=SHOQLE_VAALEDEIN_CHOICES, null=True, blank=True)
    kharide_khodro_pedari = models.CharField("توانایی خرید خودرو در خانواده پدری", max_length=1, choices=KHARIDE_KHODRO_CHOICES[1:], null=True, blank=True)
    
    tozihaat = models.TextField("دیگر توضیحات", null=True, blank=True)
    
    def __str__(self):
        return self.user.phone

    def tavallod_range(self):
        return [str(tavallod) for tavallod in range(int(self.tavallod_from), int(self.tavallod_to))]
    
    def qad_range(self):
        return [str(qad) for qad in range(int(self.qad_from), int(self.qad_to))]
    
    def vazn_range(self):
        return [str(vazn) for vazn in range(int(self.vazn_from), int(self.vazn_to))]


    class Meta:
        db_table = "entezaaraat"
        managed = True
        verbose_name = "انتظارات کاربر"
        verbose_name_plural = "انتظارات کاربران"



class Relation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", verbose_name='فرستنده')
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciver", verbose_name='گیرنده')
    status = models.CharField(max_length=1, choices=RELATION_CHOICES)
    created_at = models.DateTimeField("تاریخ ثبت درخواست", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'relations'
        managed = True
        verbose_name = 'رابطه'
        verbose_name_plural = 'رابطه ها'