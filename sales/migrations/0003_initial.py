# Generated by Django 5.0.6 on 2024-12-08 07:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0002_delete_salespartner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_type', models.CharField(choices=[('Organic', 'Organic'), ('Learning Advocate', 'Learning Advocate'), ('Learning Guide', 'Learning Guide'), ('Referrer', 'Referrer')], max_length=20)),
                ('coupon_code', models.CharField(max_length=20, unique=True)),
                ('link', models.CharField(max_length=200, unique=True)),
                ('deductible_amount', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='partner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]