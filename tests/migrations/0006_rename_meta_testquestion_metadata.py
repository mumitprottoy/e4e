# Generated by Django 5.0.6 on 2024-10-01 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_test_has_ended_alter_testanswer_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testquestion',
            old_name='meta',
            new_name='metadata',
        ),
    ]