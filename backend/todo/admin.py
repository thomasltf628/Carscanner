from django.contrib import admin
from .models import Todo, CarModel, Car_Listing

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model_name')

class Car_ListingAdmin(admin.ModelAdmin):
    list_display = ('source','make','model','year','price','mileage','location','listing_date','link_to_buyer','link_to_image')

# Register your models here.

admin.site.register(Todo, TodoAdmin),
admin.site.register(CarModel, CarModelAdmin),
admin.site.register(Car_Listing, Car_ListingAdmin),

