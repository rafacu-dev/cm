# Generated by Django 4.2.3 on 2023-07-04 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingRegistered',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('detail', models.TextField(blank=True, null=True)),
                ('color', models.TextField(blank=True, null=True)),
                ('size', models.TextField(blank=True, null=True)),
                ('smell', models.TextField(blank=True, null=True)),
                ('taste', models.TextField(blank=True, null=True)),
                ('texture', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('latitudeDelivery', models.FloatField(blank=True, null=True)),
                ('longitudeDelivery', models.FloatField(blank=True, null=True)),
                ('addressDelivery', models.TextField(blank=True, null=True)),
                ('rute', models.TextField(blank=True, default='', null=True)),
                ('key', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
        ),
    ]
