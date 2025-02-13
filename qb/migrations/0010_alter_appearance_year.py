# Generated by Django 5.0.6 on 2025-01-05 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qb', '0009_remove_university_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='year',
            field=models.CharField(choices=[('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000'), ('1999', '1999'), ('1998', '1998'), ('1997', '1997'), ('1996', '1996'), ('1995', '1995'), ('1994', '1994'), ('1993', '1993'), ('1992', '1992'), ('1991', '1991'), ('1990', '1990'), ('1989', '1989'), ('1988', '1988'), ('1987', '1987'), ('1986', '1986'), ('1985', '1985')], max_length=10),
        ),
    ]
