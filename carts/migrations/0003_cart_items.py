# Generated by Django 3.0.8 on 2020-08-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='carts.CartItem'),
        ),
    ]
