# Generated by Django 3.2.5 on 2022-11-07 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tripodsApp', '0008_catalog_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='csv',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='xml',
        ),
        migrations.AlterField(
            model_name='catalog',
            name='name',
            field=models.CharField(blank=True, default='catalog', max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='pdf',
            field=models.URLField(blank=True, null=True, verbose_name='PDF'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tripodsApp.school'),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='school',
            name='state',
            field=models.CharField(blank=True, choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default=None, max_length=2, null=True, verbose_name='State'),
        ),
    ]
