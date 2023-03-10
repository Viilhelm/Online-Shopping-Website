# Generated by Django 4.1.7 on 2023-03-06 10:54

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '__first__'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('PONumber', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('purchaseDate', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('shipped', 'shipped'), ('hold', 'hold'), ('cancelled', 'cancelled')], default='pending', max_length=20)),
                ('shipmentDate', models.DateTimeField(null=True)),
                ('cancelDate', models.DateTimeField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('myRate', models.IntegerField(default=5)),
                ('myComment', models.CharField(max_length=1000)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'unique_together': {('product', 'order')},
            },
        ),
    ]
