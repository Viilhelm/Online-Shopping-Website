# Generated by Django 4.1.7 on 2023-04-17 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_orderitem_rrdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='CanRRAgain',
            field=models.BooleanField(default=False),
        ),
    ]