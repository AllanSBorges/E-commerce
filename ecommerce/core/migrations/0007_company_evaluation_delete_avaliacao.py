# Generated by Django 4.2.7 on 2024-02-20 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_subscriber_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30, verbose_name='Nome fantasia')),
                ('company_cnpj', models.CharField(max_length=20, verbose_name='CNPJ')),
                ('company_razao_social', models.CharField(max_length=30, verbose_name='Razão Social')),
                ('company_email', models.EmailField(max_length=254)),
                ('company_phone', models.CharField(max_length=30, verbose_name='Nome fantasia')),
                ('company_store_address', models.CharField(max_length=30, verbose_name='Endereço da loja')),
                ('company_store_cep', models.IntegerField(verbose_name='CEP da loja')),
                ('company_office_address', models.CharField(max_length=30, verbose_name='Endreço do escritório')),
                ('company_office_cep', models.IntegerField(verbose_name='CEP do escritório')),
                ('company_logo_header', models.ImageField(null=True, upload_to='', verbose_name='Logo do Cabeçalho')),
                ('company_logo_footer', models.ImageField(null=True, upload_to='', verbose_name='Logo do Rodapé')),
                ('company_fav_ico', models.ImageField(null=True, upload_to='', verbose_name='Icone do site')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresa',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao', models.CharField(blank=True, max_length=30, null=True, verbose_name='Avaliação')),
                ('nota', models.IntegerField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'unique_together': {('customer_id', 'product_id')},
            },
        ),
        migrations.DeleteModel(
            name='Avaliacao',
        ),
    ]
