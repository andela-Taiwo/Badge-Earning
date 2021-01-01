# Generated by Django 3.0.9 on 2020-10-07 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201006_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField(choices=[(0, 'Mr.'), (1, 'Ms.'), (2, 'Mrs.'), (3, 'Miss.'), (4, 'Dr.')], default=0)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('address_1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('address_3', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(max_length=10, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('user_type', models.IntegerField(choices=[(0, 'Client'), (1, 'Admin')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('profile_picture_name', models.TextField(blank=True, null=True)),
                ('profile_picture_url', models.TextField(blank=True, null=True)),
                ('profile_picture_key', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]