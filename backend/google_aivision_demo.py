import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'deep-span-402803-1e142b189014.json'

client = vision.ImageAnnotatorClient()

file_name = r'orange.jpg'
image_path = f'.\picture\{file_name}'

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)
response = client.object_localization(image=image)
labels = response.localized_object_annotations


for annotation in labels:
    name = annotation.name
    score = annotation.score

    # You can use this data as needed in your Python code
    print(f"Name: {name}, Score: {score}")

