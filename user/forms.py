from  django import  forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import People


class RegistrationForm(ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = People
        fields = ['first_name', 'last_name', 'email', 'password', 'password1']

        def clean(self):
                if self.cleaned_data['password'] != self.cleaned_data['password1']:
                        raise forms.ValidationError("The passwords did not match.  Please try again.")
                return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
