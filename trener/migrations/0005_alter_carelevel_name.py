# Generated by Django 5.0 on 2024-09-04 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trener', '0004_auto_20240905_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carelevel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Poziom pielęgnacji'),
        ),
    ]
