# Generated by Django 5.0.1 on 2024-02-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_donation_app', '0004_alter_bloodbank_opositive_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbank',
            name='ABnegative_units',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='ABpositive_units',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='Anegative_units',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='Apositive_units',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='Bnegative_units',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='Bpositive_units',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
