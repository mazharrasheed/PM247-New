# Generated by Django 4.2.11 on 2024-05-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_engineer_availability_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engineer_availability',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
