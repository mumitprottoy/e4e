# Generated by Django 5.0.6 on 2024-10-13 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0006_rename_meta_testquestion_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testquestion',
            name='test',
        ),
        migrations.RemoveField(
            model_name='testanswer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='metadata',
        ),
        migrations.RemoveField(
            model_name='testquestion',
            name='question',
        ),
        migrations.AlterModelTable(
            name='markingcriterion',
            table='marking_criterion_v2',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='TestAnswer',
        ),
        migrations.DeleteModel(
            name='TestQuestion',
        ),
    ]