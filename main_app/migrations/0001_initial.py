# Generated by Django 4.1.1 on 2022-10-22 22:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=800)),
                ('location', models.CharField(max_length=100)),
                ('date_listed', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_listed'],
            },
        ),
        migrations.CreateModel(
            name='PropertyFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(choices=[('W', 'WIFI'), ('TV', 'HDTV'), ('WF', 'Waterfront'), ('CAC', 'Central Air Conditioning'), ('BS', 'Bluetooth Sound System'), ('BG', 'Board Games'), ('CH', 'Central heating'), ('P', 'Pool')], max_length=3)),
            ],
            options={
                'ordering': ['feature'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('E', 'Excellent'), ('VG', 'Very Good'), ('G', 'Good'), ('A', 'Average'), ('B', 'Bad'), ('VB', 'Very Bad'), ('S', 'Stay Away')], max_length=2)),
                ('review_text', models.TextField(max_length=800)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='property_features',
            field=models.ManyToManyField(to='main_app.propertyfeature'),
        ),
        migrations.AddField(
            model_name='property',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProfilePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.CharField(max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.property')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(verbose_name='Available from')),
                ('till_date', models.DateField(verbose_name='Available till')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.property')),
            ],
            options={
                'ordering': ['from_date'],
            },
        ),
    ]
