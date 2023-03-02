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
        return self.phone

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "users"
        managed = True
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"