# Generated by Django 3.1.1 on 2020-09-22 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddataclean',
            name='continent',
            field=models.CharField(max_length=15, null=True, unique_for_date='date'),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='iso_code',
            field=models.CharField(max_length=8, null=True, unique_for_date='date'),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='location',
            field=models.CharField(max_length=55, null=True, unique_for_date='date'),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='new_cases',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='new_deaths',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='coviddataclean',
            name='new_tests',
            field=models.IntegerField(default=0, null=True),
        ),
    ]