# Generated by Django 3.0.8 on 2020-10-24 13:42

from django.db import migrations, models

class Migration(migrations.Migration):
    
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstripe',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
