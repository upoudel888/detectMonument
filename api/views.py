# for image display on UI
from PIL import Image
from io import BytesIO
import base64
# for inference
import torch
from .inference import get_predictions # function that get predictions
# setting up paths
import os
from django.conf import settings
# for rendering showfile.html
from django.shortcuts import render,redirect

# DRF api view and Response
from rest_framework.decorators import api_view
from rest_framework.response import Response

# creating a global model that loads when api aps loads successfully
# checkout apps.py/ready(self) function
model = None
def get_model():
    global model

    if model is None:
        weights_path = os.path.join(settings.BASE_DIR, 'api', 'best.pt')
        yolo_path = os.path.join(settings.BASE_DIR,'api','yolov5')
        model =  model = torch.hub.load(yolo_path, 'custom', path = weights_path, source = 'local',device='cpu',force_reload=True)

# this endpoint receives a POST request of multipart form data from any user
# image is extracted from that form and then we get the predictions
@api_view(['POST'])
def detect_monuments(request):

    # Get the image from the request
    image = request.FILES.get('img')

    # file was not received in the request
    if(image is None):
        return Response({"error": "No file received"}, status=400)
        

    # Use PIL to open the image and get run predictions
    predictions = []
    with Image.open(image) as img:
        # squish the image to 512 * 512 i.e. create a thumbnail version of it
        img.thumbnail((512,512))
        # Get the predictions
        predictions = get_predictions(model,img)

    # Return the size in JSON format
    return Response({'predictions': predictions})


# this handles the POST request from detector app
def detect_monuments_local(request):
    if(request.method == "POST"):
        
        # Get the image from the request
        image = request.FILES.get('img')

        # file was not received in the request
        if(image is None):
            return redirect('')
        # Use PIL to open the image and run predictions
        predictions = []
        img_str = ""
        with Image.open(image) as img:
            # squish the image to 512 * 512 i.e. create a thumbnail version of it
            img.thumbnail((512,512))
            # Get the predictions
            bbox_img,predictions = get_predictions(model,img,return_raw = True)
            # convert the PIL image into byte buffer
            img_buffer = BytesIO()
            bbox_img.save(img_buffer,format="PNG")
            #encode the byte buffer as a base64 string
            img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        # creating predictions array to display in html page
        detected_classes = []
        probability_values = []
        for detection in predictions:
            detected_classes.append(detection["DetectedClass"])
            probability_values.append(detection["confidenceInClass"])

        # context to pass to the render function
        context = {"image_data" : img_str,
                   "predictions": list(zip(detected_classes,probability_values))}
        # render the contents to the UI
        return render(request,"detector/showfile.html",context) 
    
    # redirect for the back button in showfile.html
    if(request.method == "GET"):
        return redirect('')

