# Generated by Django 5.1.3 on 2024-11-06 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]