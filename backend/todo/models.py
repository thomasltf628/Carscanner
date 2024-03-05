from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class Profile(models.Model):
    picture = models.ImageField(upload_to = 'img', blank=True, null=True)
    
    def _str_(self):
        return self.picture
    

class CarModel(models.Model):
    make = models.CharField(max_length=20)
    model_name = models.CharField(max_length=40)
    """year = models.IntegerField(default=2023)
    fuel_type = models.CharField(max_length=20, default='Gasoline')
    transmission = models.CharField(max_length=15, default='Automatics')"""

    def __str__(self):
        return self.model_name

class Car_Listing(models.Model):
    source =models.CharField(max_length=50, default='Unknown') 
    make = models.CharField(max_length=50, default='Unknown')
    model = models.CharField(max_length=50)
    year = models.IntegerField(default=2023)
    price = models.FloatField()
    mileage = models.IntegerField()
    location =models.CharField(max_length=50)
    listing_date = models.DateField()
    link_to_buyer = models.URLField(
        ("Link"), 
        max_length=256, 
        db_index=True, 
        unique=False, 
        blank=True
    )
    link_to_image = models.URLField(
        ("Link"), 
        max_length=256, 
        db_index=True, 
        unique=False, 
        blank=True,
    )

