from django import forms
from .models import ClientRegister_Model

class ClientRegister_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = ClientRegister_Model
        fields = ("username", "email", "password", "phoneno", "country", "state", "city", "address", "gender")