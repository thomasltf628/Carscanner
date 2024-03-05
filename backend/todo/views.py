from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests
from .serializers import ProfileSerializer, CarModelSerializer, Car_ListingSerializer
from .models import Profile, CarModel, Car_Listing
from rest_framework.parsers import MultiPartParser, FormParser
from google.cloud import vision
from google.cloud.vision_v1 import types
import os, io
from .config import API_KEY_CarNet
import base64
import json
from django.core.files.uploadedfile import InMemoryUploadedFile

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'deep-span-402803-1e142b189014.json'

# Create your views here.

def in_memory_uploaded_file_to_bytes(file: InMemoryUploadedFile) -> bytes:

    file.seek(0)
    
    file_bytes = file.read()
    
    return file_bytes

def object_detection_google(picture):
    client = vision.ImageAnnotatorClient()
    content = picture.read()    
    image = types.Image(content=content)
    response = client.object_localization(image=image)
    labels = response.localized_object_annotations
    set_of_object_detected = {}
    for annotation in labels:
        name = annotation.name
        score = annotation.score
        set_of_object_detected[name] = score
    name_of_max_score = max(zip(set_of_object_detected.values(), set_of_object_detected.keys()))[1]
    return name_of_max_score

def object_detection_CarNet(picture):
    api_url = 'http://api.carnet.ai/v2/mmg/detect'
    Headers = {
    'Content-Type': 'application/json',
    'api-key': API_KEY_CarNet
    }
    
    file_bytes = in_memory_uploaded_file_to_bytes(picture)
    base64_image = base64.b64encode(file_bytes).decode('utf-8')
    payload = {
        'image': base64_image
        }
    json_payload = json.dumps(payload)
    try:
        response = requests.post(api_url, headers=Headers, data = json_payload)

        if response.status_code == 200:
            api_data = response.json()
            first_detection = api_data.get('detections', [])[0]

            if first_detection:
                mmg_list = first_detection.get('mmg', [])
                if mmg_list:
                    first_mmg_item = mmg_list[0]
                    generation_name = first_mmg_item.get('generation_name')
                    model_name = first_mmg_item.get('model_name')
                    make_name = first_mmg_item.get('make_name')          

            
            return generation_name, make_name, model_name

        else:

            return JsonResponse({'success': False, 'error': f'API request failed with status code {response.status_code}'})
        
    except Exception as e:

        return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer 
    parser_classes= (MultiPartParser,FormParser)

    def create(self, request, *args, **kwargs):
        picture = request.data["picture"]
        generation_name, make_name , model_name= object_detection_CarNet(picture)
        print(type(picture))

        Profile.objects.create(picture = picture)
        return JsonResponse({'generation_name': generation_name, 'make_name': make_name, 'model_name': model_name})
    

class Car_ListingViewSet(viewsets.ModelViewSet):
    queryset = Car_Listing.objects.all()
    serializer_class = Car_ListingSerializer

    def get_queryset(self):
        model_name = self.request.query_params.get('model', '')
        return Car_Listing.objects.filter(model__iexact=model_name).order_by('price')
    
"""class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()"""