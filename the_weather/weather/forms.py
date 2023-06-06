from django.forms import ModelForm, TextInput
from .models import City
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'city Name'})}

        
class UserRegister(UserCreationForm):

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        