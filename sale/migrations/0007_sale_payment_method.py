# Generated by Django 4.2.18 on 2025-02-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0006_alter_sale_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
