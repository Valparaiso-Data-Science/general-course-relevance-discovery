# Generated by Django 3.2.5 on 2022-11-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tripodsApp', '0014_catalog_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='pdf',
            field=models.CharField(default=None, max_length=200, verbose_name='PDF URL'),
        ),
    ]
