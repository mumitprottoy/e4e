# Generated by Django 5.0.6 on 2024-10-16 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_questionset_alter_markingcriterion_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testanswer',
            name='participant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tests.testparticipant'),
        ),
        migrations.AlterField(
            model_name='test',
            name='marking_criterion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.markingcriterion'),
        ),
        migrations.AlterField(
            model_name='testtimer',
            name='test',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timer', to='tests.test'),
        ),
        migrations.AlterField(
            model_name='testtimer',
            name='test_time',
            field=models.IntegerField(default=0),
        ),
    ]
