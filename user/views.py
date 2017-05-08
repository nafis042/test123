from django.http import HttpResponse,HttpResponseRedirect
from user.forms import RegistrationForm,LoginForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import People
from django.contrib.auth import authenticate, login, logout


def index(request):
    return HttpResponse("This is User Page")


def registration(request):
        if request.user.is_authenticated():
            return HttpResponse("Already In")
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                print("asche")
                user = User.objects.create_user(username=form.cleaned_data['first_name'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],

                                                )
                user.save()
                people = People(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                people.save()
                return HttpResponse('Registration Done')
            else:
                return render(request, "register.html", {'form': form})

        else:
            ''' user is not submitting the form, show them a blank registration form '''
            form = RegistrationForm()
            return render(request, "register.html", {'form': form})


def Login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "base.html")
            else:
                return render(request, "login.html", {'form': form})
        else:
            return render(request, "login.html", {'form': form})
    else:
        ''' user is not submitting the form, show the login form '''
        form = LoginForm()
        context = {'form': form}
        return render(request, "login.html", {'form': form})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')
