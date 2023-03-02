# Generated by Django 4.1.7 on 2023-03-02 14:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='شماره موبایل اشتباه میباشد', regex='^09\\d{9}$')], verbose_name='شماره موبایل')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('gender', models.CharField(choices=[('1', 'آقا'), ('2', 'خانوم')], default='1', max_length=1, verbose_name='جنسیت')),
                ('register_for', models.CharField(choices=[('1', 'خودم'), ('2', 'شخص دیگر')], default='1', max_length=1, verbose_name='ثبت نام برای')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='ابرکاربر')),
                ('is_admin', models.BooleanField(default=False, verbose_name='رابط')),
                ('is_staff', models.BooleanField(default=False, verbose_name='کارشناس')),
                ('joined_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نام')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ورود')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'db_table': 'users',
                'managed': True,
            },
        ),
    ]