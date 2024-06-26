# Generated by Django 5.0.6 on 2024-05-10 09:45

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0003_rename_engineer_availablity_engineer_availability'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWithEngineerAvailability',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='engineer_availability',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='engineer_availability',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='engineer_availability',
            name='engineer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='engineer_availability',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
