# Generated by Django 5.0.6 on 2024-09-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loyalty_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
