# Generated by Django 3.0.8 on 2023-01-28 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0002_poster_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
