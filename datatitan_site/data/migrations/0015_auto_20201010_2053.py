# Generated by Django 3.1.2 on 2020-10-11 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20201002_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddataclean',
            name='stringency_index',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
