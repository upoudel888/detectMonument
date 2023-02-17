from PIL import Image
from .inference import get_predictions

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def detect_image(request):
    # Get the image from the request
    image = request.FILES.get('img')

    # Use PIL to open the image and get its size
    predictions = []
    with Image.open(image) as img:
        predictions = get_predictions(img)

    # Return the size in JSON format
    return Response({'predictions': predictions})


