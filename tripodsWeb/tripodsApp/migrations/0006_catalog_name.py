# Generated by Django 3.2.5 on 2022-10-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tripodsApp', '0005_auto_20221017_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='School name'),
        ),
    ]