# Generated by Django 4.2.7 on 2024-02-21 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_company_company_office_cep_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Company',
        ),
    ]
