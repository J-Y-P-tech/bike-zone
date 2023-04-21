from django.db import models
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
import uuid
import os


def bikes_image_file_path(instance, filename):
    """ Generate file path for new image """

    # get file extension
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    # This ensures that the path is created according to
    # the operating system that we are running on
    return os.path.join('uploads', 'img', filename)


class Bike(models.Model):
    state_choice = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District Of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )

    year_choice = []
    for r in range(2000, (datetime.now().year + 1)):
        year_choice.append((r, r))

    features_choices = (
        ('Dual-Channel ABS', 'Dual-Channel ABS'),
        ('Rear Lift Prevention', 'Rear Lift Prevention'),
        ('Adjustable Suspension', 'Adjustable Suspension'),
        ('Hazard Lights', 'Hazard Lights'),
        ('Adjustable Clutch and Brake Levers', 'Adjustable Clutch and Brake Levers'),
        ('Performance Tyres', 'Performance Tyres'),
        ('Liquid Cooling', 'Liquid Cooling'),
        ('Crash Protection Accessories', 'Crash Protection Accessories'),
        ('Reversing Camera', 'Reversing Camera'),
        ('Direct Fuel Injection', 'Direct Fuel Injection'),
        ('Auto Start/Stop', 'Auto Start/Stop'),
        ('Bluetooth Handset', 'Bluetooth Handset'),
    )

    bike_title = models.CharField(max_length=255)
    state = models.CharField(choices=state_choice, max_length=100)
    city = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(('year'), choices=year_choice)
    condition = models.CharField(max_length=100)
    price = models.IntegerField()
    description = RichTextField()
    bike_photo = models.ImageField(upload_to=bikes_image_file_path)
    bike_photo_1 = models.ImageField(upload_to=bikes_image_file_path, blank=True)
    bike_photo_2 = models.ImageField(upload_to=bikes_image_file_path, blank=True)
    bike_photo_3 = models.ImageField(upload_to=bikes_image_file_path, blank=True)
    bike_photo_4 = models.ImageField(upload_to=bikes_image_file_path, blank=True)
    features = MultiSelectField(choices=features_choices, blank=True)

    # STANDARD, CRUISER, SPORT BIKE, TOURING, SPORT TOURING, DUAL SPORT
    body_style = models.CharField(max_length=100)

    # Internal Combustion Engines (ICE), Electric Motors, Hybrid Engines
    engine = models.CharField(max_length=100)

    # chain, belt or shaft
    transmission = models.CharField(max_length=100)

    miles = models.IntegerField()
    vin_no = models.CharField(max_length=100)
    milage = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    no_of_owners = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.bike_title
