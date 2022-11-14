# Generated by Django 3.2.5 on 2022-10-17 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tripodsApp', '0003_auto_20221017_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='school_id',
        ),
        migrations.RemoveField(
            model_name='request',
            name='name',
        ),
        migrations.RemoveField(
            model_name='request',
            name='year',
        ),
        migrations.RemoveField(
            model_name='school',
            name='csv',
        ),
        migrations.RemoveField(
            model_name='school',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='school',
            name='year',
        ),
        migrations.AddField(
            model_name='school',
            name='catalog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tripodsApp.catalog'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='school',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]