# Generated by Django 4.2 on 2023-08-23 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_membership_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='allowed_tests',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='allowed_words',
            field=models.IntegerField(null=True),
        ),
    ]
