# Generated by Django 3.0.8 on 2020-08-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_auto_20200809_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]