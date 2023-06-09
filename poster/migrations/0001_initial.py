# Generated by Django 4.2.3 on 2023-07-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='poster')),
                ('dimension', models.FloatField()),
                ('text', models.TextField()),
                ('color', models.IntegerField(blank=True, null=True)),
                ('font', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaticPoster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='static_poster')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
