from django import forms
from .models import UserImages

# yesari garda form.save() gareko matlab nai vayena ni 
# class ImageForm(forms.Form):
#     name = forms.CharField(max_length=15,required=True)
#     img = forms.ImageField(required=True)


class UserImagesForm(forms.ModelForm):
    
    class Meta:
        model = UserImages
        fields = ("img",)
