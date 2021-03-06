# Generated by Django 3.0.8 on 2020-08-09 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=30),
        ),
    ]
