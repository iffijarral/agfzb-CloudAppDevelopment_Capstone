from django.db import models
from django.utils.timezone import now


# Create your models here.
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Audi')
    description = models.CharField(null=True, max_length=200)
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'Suv'
    WAGON = 'Wagon'    
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon'),        
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='A6')
    dealer_id = models.IntegerField(default=1)
    type_choice = models.CharField(
        null=False,      
        choices=TYPE_CHOICES,
        default=SEDAN,
        max_length=20,
    )
    year = models.DateField(default=now)
    def __str__(self):
         return "Name: " + self.name + "," + \
               "make: " + self.make.name + "," + \
               "type: " + self.type_choice 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year):
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year   