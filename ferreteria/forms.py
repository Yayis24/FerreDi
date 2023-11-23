from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modificar mensajes de ayuda y etiquetas según tus preferencias
        self.fields['username'].help_text = ''
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirmar contraseña'
