# Generated by Django 5.0.6 on 2024-07-16 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb', '0004_delete_questionmeta'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='meta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='qb.questionmetadata'),
        ),
    ]
