from rest_framework import serializers
from .models import Profile, CarModel, Car_Listing

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "picture"]

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields =['id','make','model_name']
        """field =['id','make','model_name','year','fuel_type','transmission']"""

class Car_ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car_Listing
        fields ='__all__'
        """field = ['source','make','model', 'year','price',
        'mileage','location','listing_date','link_to_buyer','link_to_image']"""

"""class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')"""