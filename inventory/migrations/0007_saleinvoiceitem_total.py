# Generated by Django 4.1.7 on 2023-05-23 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_brand_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleinvoiceitem',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
