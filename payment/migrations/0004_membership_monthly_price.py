# Generated by Django 4.2 on 2023-08-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_membership_allowed_tests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='monthly_price',
            field=models.FloatField(default=10, null=True),
        ),
    ]
