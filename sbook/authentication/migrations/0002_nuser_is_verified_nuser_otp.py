# Generated by Django 4.2.8 on 2024-01-09 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]