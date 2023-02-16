from PIL import Image

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def detect_image(request):
    # Get the image from the request
    image = request.FILES.get('img')

    # Use PIL to open the image and get its size
    
    with Image.open(image) as img:
        width, height = img.size

    # Return the size in JSON format
    return Response({'width': width, 'height': height})


