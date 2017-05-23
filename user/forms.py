from  django import  forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import People, File, Plot, Public


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


class UploadForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']


class UpdateForm(ModelForm):
    class Meta:
        model = Plot
        fields = ['area_id', 'plot_id', 'name', 'description', 'lat', 'lng', 'alt', 'type', 'polygon']


class UpdatePublicForm(ModelForm):
    class Meta:
        model = Public
        fields = ['plot_code', 'floor_id', 'name', 'description', 'lat', 'lng', 'alt', 'type', 'polygon']