from distutils.log import error
from logging import exception
from django import forms
from .models import Task, User

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title","description","complete"]

        widgets = {
            "title": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            "description": forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción', 'id':'txt','onkeyup':'textAreaAdjust(this)'}),
            'complete': forms.CheckboxInput(attrs={'class':'form-check-input','type':'checkbox','role':'switch'})
        }

class InicioForm (AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super(InicioForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingresar nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password'].widget.attrs['type'] = 'password'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingresar contraseña'

class RegistroForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
        'numerical' : 'La contraseña no puede ser completamente numérica.'
    }

    username = forms.CharField(max_length=30,)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese su nombre de usuario'
        self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password1'].widget.attrs['placeholder'] = 'Ingrese su contraseña'
        self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password2'].widget.attrs['placeholder'] = 'Vuelva a ingresar su contraseña'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2' )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password2.isdigit():
            raise ValidationError(
                self.error_messages['numerical'],
                code='numerical',
            )

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    @property
    def errors(self):
        """Return an ErrorDict for the data provided for the form."""
        if self._errors is None:
            self.full_clean()

        error = dict(self._errors)
        mensaje = [*error.values()]

        return mensaje
    

