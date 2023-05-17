import os
from PIL import Image
from ...models import Bike
import DuckDuckGoImages as ddg
from django.db import transaction
from django.utils import timezone
from django.core.files import File
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
import tempfile

bikes_data = [
    {
        "bike_title": "BMW S1000RR",
        "state": "CA",
        "city": "Los Angeles",
        "color": "Black",
        "model": "S1000RR",
        "year": "2018",
        "condition": "Excellent, well maintained, low mileage",
        "price": 15000,
        "description": "The ultimate superbike with 199 hp, dynamic traction control, ABS, quickshifter and four riding modes. A blast to ride on the track or the street.",
        "body_style": "Sport",
        "engine": "999 cc inline-four",
        "transmission": "6-speed",
        "miles": 5000,
        "vin_no": "WB10D2109JZ353789",
        "milage": 40,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": True
    },
    {
        "bike_title": "Ducati Multistrada 1200",
        "state": "NY",
        "city": "New York",
        "color": "Red",
        "model": "Multistrada 1200",
        "year": "2016",
        "condition": "Very good, minor scratches, serviced regularly",
        "price": 12000,
        "description": "The versatile adventure bike with 150 hp, four riding modes, traction control, ABS and semi-active suspension. Ready for any road or trail.",
        "body_style": "Adventure",
        "engine": "1198 cc L-twin",
        "transmission": "6-speed",
        "miles": 10000,
        "vin_no": "ZDM12BSW7GB012345",
        "milage": 35,
        "fuel_type": "Gasoline",
        "no_of_owners": 2,
        "is_featured": False
    },
    {
        "bike_title": "BMW K1600GTL",
        "state": "FL",
        "city": "Miami",
        "color": "Blue",
        "model": "K1600GTL",
        "year": "2017",
        "condition": "Like new, garage kept, no accidents",
        "price": 18000,
        "description": "The ultimate luxury touring bike with 160 hp, six-cylinder engine, adaptive headlight, electronic suspension, heated seats and grips, and a large top case.",
        "body_style": "Touring",
        "engine": "1649 cc inline-six",
        "transmission": "6-speed",
        "miles": 8000,
        "vin_no": "WB1061201HZF97865",
        "milage": 30,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": True
    },
    {
        "bike_title": "Harley-Davidson Street Glide",
        "state": "TX",
        "city": "Houston",
        "color": "Black",
        "model": "Street Glide",
        "year": "2018",
        "condition": "Mint condition, custom paint and exhaust, lots of extras",
        "price": 20000,
        "description": "The iconic bagger with 107 cu in Milwaukee-Eight engine, batwing fairing, Boom! Box infotainment system, cruise control and ABS.",
        "body_style": "Bagger",
        "engine": "1746 cc V-twin",
        "transmission": "6-speed",
        "miles": 6000,
        "vin_no": "1HD1KBC19JB678901",
        "milage": 25,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": False
    },
    {
        "bike_title": "KTM 250 XC-W TPI",
        "state": "CO",
        "city": "Denver",
        "color": "Orange",
        "model": "250 XC-W TPI",
        "year": "2018",
        "condition": "Good, some wear and tear, runs great",
        "price": 7000,
        "description": "The first fuel-injected two-stroke bike with 249 cc engine, transfer port injection, electric starter, WP suspension and Brembo brakes.",
        "body_style": "Enduro",
        "engine": "249 cc single-cylinder",
        "transmission": "6-speed",
        "miles": 3000,
        "vin_no": "VBKXWL237JM123456",
        "milage": 50,
        "fuel_type": "Gasoline",
        "no_of_owners": 2,
        "is_featured": False
    },
    {
        "bike_title": "Honda CB500F",
        "state": "WA",
        "city": "Seattle",
        "color": "Red",
        "model": "CB500F",
        "year": "2015",
        "condition": "Fair, some scratches and dents, needs new tires",
        "price": 3000,
        "description": "The perfect beginner bike with 471 cc parallel-twin engine, low seat height, light weight and easy handling.",
        "body_style": "Naked",
        "engine": "471 cc parallel-twin",
        "transmission": "6-speed",
        "miles": 15000,
        "vin_no": "MLHPC4560F5100001",
        "milage": 45,
        "fuel_type": "Gasoline",
        "no_of_owners": 3,
        "is_featured": False
    },
    {
        "bike_title": "Yamaha YZF-R1",
        "state": "NV",
        "city": "Las Vegas",
        "color": "Blue",
        "model": "YZF-R1",
        "year": "2017",
        "condition": "Very good, minor scratches, serviced regularly",
        "price": 14000,
        "description": "The legendary superbike with 998 cc crossplane engine, MotoGP-inspired electronics, traction control, slide control, ABS and quickshifter.",
        "body_style": "Sport",
        "engine": "998 cc inline-four",
        "transmission": "6-speed",
        "miles": 7000,
        "vin_no": "JYARN39E9HA000001",
        "milage": 40,
        "fuel_type": "Gasoline",
        "no_of_owners": 2,
        "is_featured": False
    },
    {
        "bike_title": "Kawasaki Ninja 300",
        "state": "IL",
        "city": "Chicago",
        "color": "Green",
        "model": "Ninja 300",
        "year": "2014",
        "condition": "Good, some wear and tear, runs great",
        "price": 3500,
        "description": "The popular beginner bike with 296 cc parallel-twin engine, slipper clutch, optional ABS and sporty styling.",
        "body_style": "Sport",
        "engine": "296 cc parallel-twin",
        "transmission": "6-speed",
        "miles": 12000,
        "vin_no": "JKAEX8A1XEA000001",
        "milage": 50,
        "fuel_type": "Gasoline",
        "no_of_owners": 2,
        "is_featured": False
    },
    {
        "bike_title": "Suzuki Hayabusa",
        "state": "AZ",
        "city": "Phoenix",
        "color": "Silver",
        "model": "Hayabusa",
        "year": "2013",
        "condition": "Excellent, well maintained, low mileage",
        "price": 10000,
        "description": "The world's fastest production motorcycle with 1340 cc inline-four engine, 197 hp, dual throttle valves, ABS and aerodynamic design.",
        "body_style": "Sport",
        "engine": "1340 cc inline-four",
        "transmission": "6-speed",
        "miles": 4000,
        "vin_no": "JS1GX72B8D2100001",
        "milage": 30,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": True
    },
    {
        "bike_title": "Triumph Bonneville T120",
        "state": "OR",
        "city": "Portland",
        "color": "Black",
        "model": "Bonneville T120",
        "year": "2018",
        "condition": "Like new, garage kept, no accidents",
        "price": 9000,
        "description": "The classic retro bike with 1200 cc parallel-twin engine, ride-by-wire throttle, traction control, ABS and heated grips.",
        "body_style": "Retro",
        "engine": "1200 cc parallel-twin",
        "transmission": "6-speed",
        "miles": 3000,
        "vin_no": "SMTD40HL9JT860001",
        "milage": 45,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": False
    },
    {
        "bike_title": "Honda Gold Wing",
        "state": "GA",
        "city": "Atlanta",
        "color": "White",
        "model": "Gold Wing",
        "year": "2018",
        "condition": "Like new, garage kept, no accidents",
        "price": 22000,
        "description": "The ultimate luxury touring bike with 1833 cc flat-six engine, seven-speed DCT, reverse gear, airbag, navigation system and heated seats.",
        "body_style": "Touring",
        "engine": "1833 cc flat-six",
        "transmission": "7-speed DCT",
        "miles": 2000,
        "vin_no": "JH2SC791XJK000001",
        "milage": 35,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": True
    },
    {
        "bike_title": "Ducati Panigale V4",
        "state": "NJ",
        "city": "Newark",
        "color": "Red",
        "model": "Panigale V4",
        "year": "2018",
        "condition": "Excellent, well maintained, low mileage",
        "price": 18000,
        "description": "The stunning superbike with 1103 cc V4 engine, 214 hp, traction control, wheelie control, slide control, ABS and quickshifter.",
        "body_style": "Sport",
        "engine": "1103 cc V4",
        "transmission": "6-speed",
        "miles": 4000,
        "vin_no": "ZDMFAKBW9JB000001",
        "milage": 30,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": False
    },
    {
        "bike_title": "Kawasaki Z900RS",
        "state": "NC",
        "city": "Charlotte",
        "color": "Brown",
        "model": "Z900RS",
        "year": "2018",
        "condition": "Like new, garage kept, no accidents",
        "price": 9000,
        "description": "The retro-styled naked bike with 948 cc inline-four engine, traction control, ABS and LED lights.",
        "body_style": "Naked",
        "engine": "948 cc inline-four",
        "transmission": "6-speed",
        "miles": 3000,
        "vin_no": "JKAZR2C1XJA000001",
        "milage": 40,
        "fuel_type": "Gasoline",
        "no_of_owners": 1,
        "is_featured": False
    },
    {
        "bike_title": "Honda CRF250L Rally",
        "state": "UT",
        "city": "Salt Lake City",
        "color": "Red",
        "model": "CRF250L Rally",
        "year": "2017",
        "condition": "Good, some wear and tear, runs great",
        "price": 4000,
        "description": "The adventure-ready dual-sport bike with 249 cc single-cylinder engine, long-travel suspension, windscreen, handguards and ABS.",
        "body_style": "Dual-sport",
        "engine": "249 cc single-cylinder",
        "transmission": "6-speed",
        "miles": 8000,
        "vin_no": "MLHMD4412H5000001",
        "milage": 60,
        "fuel_type": "Gasoline",
        "no_of_owners": 2,
        "is_featured": False
    },
    {
        "bike_title": "Yamaha FZ-07",
        "state": "MN",
        "city": "Minneapolis",
        "color": "Gray",
        "model": "FZ-07",
        "year": "2015",
        "condition": "Fair, some scratches and dents, needs new tires",
        "price": 4000,
        "description": "The fun and affordable naked bike with 689 cc parallel-twin engine, crossplane crankshaft, lightweight chassis and ABS.",
        "body_style": "Naked",
        "engine": "689 cc parallel-twin",
        "transmission": "6-speed",
        "miles": 10000,
        "vin_no": "JYARM06E7FA000001",
        "milage": 50,
        "fuel_type": "Gasoline",
        "no_of_owners": 3,
        "is_featured": False
    }

]


class Command(BaseCommand):
    """ Django command to populate the Bike model.

    This command deletes all bike records and corresponding images
    from the database and docker volume,
    and then populates the model with data based on a pre-defined list.
    For each bike in the list,
    up to 5 images are downloaded from DuckDuckGo based on the bike's
    attributes (title, color, and year),
    saved to disk, and associated with the bike record.
    """

    def __init__(self):
        # self.folder_path = 'dwnld'
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder_path = self.temp_dir.name
        self.filename = "blue_image.jpg"
        self.bikes_data = bikes_data
        self.bike_data = []

    def delete_all_files_in_folder(self):
        """
        Deletes all files and folders located in a specified folder path.
        Args: folder_path (str): The path to the folder to be emptied.
        Returns: None
        Raises: None
        """
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    @staticmethod
    def clear_all_bikes_data():
        """
        Deletes all bike records from the database and corresponding images
        from the docker volume.
        This function gets all the bike records from the database and loops
        through each record.
        For each record, it checks if the corresponding bike photos exist in
        the docker volume and deletes them if they do.
        Then, it deletes the bike record from the database. This function
        should be called with caution
        as it permanently deletes all bike data and corresponding images.

        Raises: Any exception raised during the deletion of bike photos
        or bike records will be propagated.
        Returns: None
        """

        with transaction.atomic():
            # Get all the bike records
            bikes = Bike.objects.all()
            # Loop through each bike record
            for bike in bikes:
                # Delete the bike photos from the docker volume if they exist
                if bike.bike_photo:
                    default_storage.delete(bike.bike_photo.name)
                if bike.bike_photo_1:
                    default_storage.delete(bike.bike_photo_1.name)
                if bike.bike_photo_2:
                    default_storage.delete(bike.bike_photo_2.name)
                if bike.bike_photo_3:
                    default_storage.delete(bike.bike_photo_3.name)
                if bike.bike_photo_4:
                    default_storage.delete(bike.bike_photo_4.name)
                # Delete the bike record from the database
                bike.delete()

    def populate_bikes(self):
        """
        Populates the database with bikes based on data from a pre-defined list
        (`bikes_data`). For each bike in the list, downloads up to 5 images from
        DuckDuckGo based on the bike's attributes (title, color, and year),
        saves the images to disk, and creates a new Bike object in the database
        with the bike's attributes and image files.
        If the folder where the images are saved is empty, creates a blue
        square image and saves it as the bike's primary image (`bike_photo`).
        If there are more than one image in the folder, the function saves them as
        additional images (`bike_photo_1`, `bike_photo_2`, etc.) associated with
        the bike record.
        """

        # loop through the bikes_data list
        for bike_data in bikes_data:

            # delete all data from dwnld
            self.delete_all_files_in_folder()

            self.bike_data = bike_data

            ddg.download(bike_data['bike_title'] + " color " +
                         bike_data['color'] + " year " +
                         str(bike_data['year']),
                         max_urls=5,
                         folder=self.folder_path)

            # create a new Bike object with the data from the JSON
            bike = Bike.objects.create(
                bike_title=bike_data['bike_title'],
                state=bike_data['state'],
                city=bike_data['city'],
                color=bike_data['color'],
                model=bike_data['model'],
                year=bike_data['year'],
                condition=bike_data['condition'],
                price=bike_data['price'],
                description=bike_data['description'],
                body_style=bike_data['body_style'],
                engine=bike_data['engine'],
                transmission=bike_data['transmission'],
                miles=bike_data['miles'],
                vin_no=bike_data['vin_no'],
                milage=bike_data['milage'],
                fuel_type=bike_data['fuel_type'],
                no_of_owners=bike_data['no_of_owners'],
                is_featured=bike_data['is_featured']
            )

            # check if the folder contains any images
            if not os.listdir(self.folder_path):
                image = Image.new('RGB', (600, 600), color='blue')
                file_path = os.path.join(self.folder_path, self.filename)
                image.save(file_path)
                first_image = os.listdir(self.folder_path)[0]
                image_file = File(open(os.path.join(self.folder_path, first_image), 'rb'))
                bike.bike_photo.save(first_image, image_file)
            else:
                # if there are images, use the first one as bike_photo
                first_image = os.listdir(self.folder_path)[0]
                image_file = File(open(os.path.join(self.folder_path, first_image), 'rb'))
                bike.bike_photo.save(first_image, image_file)

                # if there are more than one images, save them to bike_photo_1, bike_photo_2, etc.
                if len(os.listdir(self.folder_path)) > 1:
                    for i, image_path in enumerate(os.listdir(self.folder_path)[1:5], start=1):
                        image_file = File(open(os.path.join(self.folder_path, image_path), 'rb'))
                        setattr(bike, f'bike_photo_{i}', image_file)

            bike.save()

    def handle(self, *args, **options):
        """ Entrypoint for command. """
        # number_of_bikes = Bike.objects.all().count()
        self.clear_all_bikes_data()
        # if number_of_bikes < 1:
        self.populate_bikes()
