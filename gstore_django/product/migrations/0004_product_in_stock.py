# Generated by Django 4.1.7 on 2023-03-29 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_alter_product_options_alter_category_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="in_stock",
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
