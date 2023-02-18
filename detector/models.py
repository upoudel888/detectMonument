from django.db import models
import uuid
import os

def generate_filename(instance,filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('inferenceImages/', filename)
    

class UserImages(models.Model):
    img = models.ImageField(upload_to=generate_filename,null=True,blank=False)
# Create your models here.
