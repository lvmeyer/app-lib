# Generated by Django 3.2.16 on 2023-01-29 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20230125_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='localization',
            name='zipCode',
            field=models.IntegerField(default=0),
        ),
    ]