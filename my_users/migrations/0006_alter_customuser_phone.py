# Generated by Django 5.1.6 on 2025-03-15 00:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_users', '0005_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Telefon raqamida kamida 9ta No str!  bo'lishi kerak.", regex='^\\+998[0-9]{9}$')]),
        ),
    ]
