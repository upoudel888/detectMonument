from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from PIL import Image

# # Create your views here.
# def sayHello(request):
#     context = {
#         "form" : forms.UserImagesForm()
#     }
#     if( request.method == "GET"):
#         return render(request,"detector/index.html",context)

#     if(request.method == "POST"):
#         form = forms.UserImagesForm(request.POST,request.FILES)
#         print(request.FILES)
#         if(form.is_valid()):
#             instance = form.save()
#             context = {
#                 "form" : forms.UserImagesForm(),
#                 "submit_success" : True,
#                 "img_obj" : instance.img.url
#             }

#             print("Valid Context")
#             print(context)
#             return render(request,"detector/index.html",context)
#         else:
#             print("Invalid")
#             return render(request,"detector/index.html",context)

# Create your views here.
def sayHello(request):
    context = {
        "form" : forms.UserImagesForm()
    }
    if( request.method == "GET"):
        return render(request,"detector/index.html",context)

    if(request.method == "POST"):
        form = forms.UserImagesForm(request.POST,request.FILES)
        if(form.is_valid()):
            instance = form.save()
            context = {
                "form" : forms.UserImagesForm(),
                "submit_success" : True,
                "img_obj" : instance.img.url
            }

            print("Valid Context")
            print(context)
            return render(request,"detector/index.html",context)
        else:
            print("Invalid")
            return render(request,"detector/index.html",context)
        
