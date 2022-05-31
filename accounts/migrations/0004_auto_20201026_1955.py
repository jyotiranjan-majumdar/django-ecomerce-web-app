# Generated by Django 3.0.8 on 2020-10-26 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_emailconfirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailconfirmed',
            name='hashkey',
        ),
        migrations.AddField(
            model_name='emailconfirmed',
            name='activation_key',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]