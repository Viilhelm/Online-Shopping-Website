# Generated by Django 4.1.7 on 2023-04-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_avgrating'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['productName', 'id'], name='products_pr_product_437f71_idx'),
        ),
    ]
