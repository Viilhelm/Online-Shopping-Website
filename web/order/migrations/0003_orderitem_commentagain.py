# Generated by Django 4.1.7 on 2023-04-11 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_orderitem_mycomment_alter_orderitem_myrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='commentAgain',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]