import torch
from PIL import Image
from .inference import get_predictions # function that get predictions
import os
from django.conf import settings

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

    # lazy loading the model
    get_model()
    # Get the image from the request
    image = request.FILES.get('img')

    # Use PIL to open the image and get its size
    predictions = []
    with Image.open(image) as img:
        predictions = get_predictions(model,img)

    # Return the size in JSON format
    return Response({'predictions': predictions})

@api_view(['POST'])
def detect_monuments_local(request):

    # lazy loading the model
    get_model()
    # Get the image from the request
    image = request.FILES.get('img')

    # Use PIL to open the image and get its size
    predictions = []
    with Image.open(image) as img:
        predictions = get_predictions(model,img)

    # Return the size in JSON format
    return Response({'predictions': predictions})
