# Generated by Django 4.1.7 on 2023-05-23 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_saleinvoice_voided'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleinvoiceitem',
            name='sale_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_items', to='inventory.saleinvoice'),
        ),
    ]
