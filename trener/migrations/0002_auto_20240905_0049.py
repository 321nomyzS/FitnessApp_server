# Generated by Django 5.0 on 2024-09-04 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trener', '0001_initial'),
    ]


    operations = [
        migrations.CreateModel(
            name='LightRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Wymagania świetlne')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
            ],
        ),
    ]
