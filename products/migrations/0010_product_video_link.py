# Generated by Django 3.1.2 on 2020-10-19 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_can_backorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='video_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
