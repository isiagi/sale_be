# Generated by Django 4.2.18 on 2025-02-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
