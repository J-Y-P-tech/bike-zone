# Generated by Django 3.2.18 on 2023-04-20 08:53

import ckeditor.fields
import datetime
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike_title', models.CharField(max_length=255)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District Of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], verbose_name='year')),
                ('condition', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('description', ckeditor.fields.RichTextField()),
                ('bike_photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('bike_photo_1', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('bike_photo_2', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('bike_photo_3', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('bike_photo_4', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('features', multiselectfield.db.fields.MultiSelectField(choices=[('Dual-Channel ABS', 'Dual-Channel ABS'), ('Rear Lift Prevention', 'Rear Lift Prevention'), ('Adjustable Suspension', 'Adjustable Suspension'), ('Hazard Lights', 'Hazard Lights'), ('Adjustable Clutch and Brake Levers', 'Adjustable Clutch and Brake Levers'), ('Performance Tyres', 'Performance Tyres'), ('Liquid Cooling', 'Liquid Cooling'), ('Crash Protection Accessories', 'Crash Protection Accessories'), ('Reversing Camera', 'Reversing Camera'), ('Direct Fuel Injection', 'Direct Fuel Injection'), ('Auto Start/Stop', 'Auto Start/Stop'), ('Bluetooth Handset', 'Bluetooth Handset')], max_length=243)),
                ('body_style', models.CharField(max_length=100)),
                ('engine', models.CharField(max_length=100)),
                ('transmission', models.CharField(max_length=100)),
                ('miles', models.IntegerField()),
                ('vin_no', models.CharField(max_length=100)),
                ('milage', models.IntegerField()),
                ('fuel_type', models.CharField(max_length=50)),
                ('no_of_owners', models.CharField(max_length=100)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
