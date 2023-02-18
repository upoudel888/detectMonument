import torch
from PIL import Image
from .inference import get_predictions
import os
from django.conf import settings
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

model = None

def get_model():
    global model

    if model is None:
        weights_path = os.path.join(settings.BASE_DIR, 'api', 'yolov5', 'weights', 'best.pt')
        yolo_path = os.path.join(settings.BASE_DIR,'api','yolov5')
        model =  model = torch.hub.load(yolo_path, 'custom', path = weights_path, source = 'local',device='cpu',force_reload=True)

@api_view(['POST'])
def detect_image(request):

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


