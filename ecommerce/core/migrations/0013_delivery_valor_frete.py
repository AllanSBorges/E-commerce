# Generated by Django 4.2.7 on 2024-04-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_codigo_entrega_delivery_codigo_rastreio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='valor_frete',
            field=models.DecimalField(decimal_places=2, default=35, max_digits=7),
            preserve_default=False,
        ),
    ]
