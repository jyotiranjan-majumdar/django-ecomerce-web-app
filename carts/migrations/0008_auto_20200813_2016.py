# Generated by Django 3.0.8 on 2020-08-13 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_variation_category'),
        ('carts', '0007_auto_20200812_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(to='products.Variation'),
        ),
    ]