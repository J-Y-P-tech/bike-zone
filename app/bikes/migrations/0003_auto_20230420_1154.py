# Generated by Django 3.2.18 on 2023-04-20 11:54

from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0002_auto_20230420_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bike',
            name='features',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Dual-Channel ABS', 'Dual-Channel ABS'), ('Rear Lift Prevention', 'Rear Lift Prevention'), ('Adjustable Suspension', 'Adjustable Suspension'), ('Hazard Lights', 'Hazard Lights'), ('Adjustable Clutch and Brake Levers', 'Adjustable Clutch and Brake Levers'), ('Performance Tyres', 'Performance Tyres'), ('Liquid Cooling', 'Liquid Cooling'), ('Crash Protection Accessories', 'Crash Protection Accessories'), ('Reversing Camera', 'Reversing Camera'), ('Direct Fuel Injection', 'Direct Fuel Injection'), ('Auto Start/Stop', 'Auto Start/Stop'), ('Bluetooth Handset', 'Bluetooth Handset')], max_length=243),
        ),
    ]
