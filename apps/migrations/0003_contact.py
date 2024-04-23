# Generated by Django 5.0.4 on 2024-04-23 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_booking_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='noreply@example.com', max_length=254, verbose_name='Email')),
                ('issue', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=5000)),
            ],
        ),
    ]
