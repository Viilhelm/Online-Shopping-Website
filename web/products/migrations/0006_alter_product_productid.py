# Generated by Django 4.1.7 on 2023-02-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_categoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productID',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
