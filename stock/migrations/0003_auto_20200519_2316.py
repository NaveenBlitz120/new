# Generated by Django 3.0.5 on 2020-05-19 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20200519_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='company_name',
        ),
        migrations.DeleteModel(
            name='company',
        ),
        migrations.DeleteModel(
            name='medicine',
        ),
    ]
