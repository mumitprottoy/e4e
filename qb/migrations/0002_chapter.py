# Generated by Django 5.0.6 on 2024-07-14 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
