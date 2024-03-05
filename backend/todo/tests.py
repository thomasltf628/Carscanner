import requests
import base64
import json

def make_mmg_detection_request(image_path):
    # Replace 'your_api_key' with your actual API key
    api_key = 'c2b9951a-ae52-452f-8561-60026f8f3d53'
    
    # API endpoint from the provided Swagger documentation
    api_url = 'http://api.carnet.ai/v2/mmg/detect'

    # Headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'api-key': 
    }

    # Read the image file as binary data
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    base64_image = base64.b64encode(image_data).decode('utf-8')
    # JSON payload with the image data
    payload = {
        'image': base64_image
    }
    json_payload = json.dumps(payload)
    # Make the POST request
    response = requests.post(api_url, headers=headers, data=json_payload)

    # Handle the response
    if response.status_code == 200:
        # Successful response
        result = response.json()
        return result
    else:
        # Error handling
        return {'error': f'Request failed with status code {response.status_code}'}

# Example usage
image_path = r'C:\Users\super\Capstone_project\backend\picture\Benz_GLE.jpg'
result = make_mmg_detection_request(image_path)
print(result)