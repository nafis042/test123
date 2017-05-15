from django.http import HttpResponse, HttpResponseRedirect
from user.forms import RegistrationForm, LoginForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import People, Plot, Public, Area
from . import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework import  viewsets
from .serializers import PeopleSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from fastkml import kml


def index(request):
    return HttpResponse("This is User Page")


def registration(request):
        if request.user.is_authenticated():
            return HttpResponse("Already In")
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
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
        return render(request, "login.html", {'form': form})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')


@permission_classes([])
class PeopleList(viewsets.ModelViewSet):

    queryset = People.objects.all()
    serializer_class = serializers.PeopleSerializer

    def perform_create(self, serializer):
        # serializer.validated_data.update({'company_id': get_company_id(self.request)})
        super().perform_create(serializer)

    def get_queryset(self):
        return super().get_queryset()


@permission_classes([IsAuthenticated])
class UserList(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_create(self, serializer):
        # serializer.validated_data.update({'company_id': get_company_id(self.request)})
        super().perform_create(serializer)

    def get_queryset(self):
        return super().get_queryset()


def parse(request):
    with open('plot.kml', 'r') as myfile:
        data = myfile.read()

   # print(data)
    k = kml.KML()
    k.from_string(data)
    features = list(k.features())
    print(len(features))
    f2 = list(features[0].features())
    print(len(f2))
    for i in f2:
        print(i.name+" "+i.description+" "+str(i.geometry))

        if "POINT" in str(i.geometry):
           # print("asche")
            temp = str(i.geometry).replace("POINT (", "").replace(")", "")
            temp1 = temp.split()
            latitude = temp1[0]
            longitude = temp1[1]
            altitude = temp1[2]
            poly = "NULL"
            print(latitude+" "+longitude+" "+altitude)
        else:
            poly = str(i.geometry).replace("POLYGON((", "").replace("))", "")
            latitude = "NULL"
            longitude = "NULL"
            altitude = "NULL"
            print(poly)

        name = str(i.name)

        # area_id plot_id description type [optional-floor_id]
        total = str(i.description).split()
        if len(total) == 4:
            area = Area.objects.get(pk=int(total[0]))
            plot = int(total[1])
            descript = total[2]
            type = total[3]

            plot = Plot(area_id=area,
                        plot_id=plot,
                        name=name,
                        description=descript,
                        lat=latitude,
                        lng=longitude,
                        alt=altitude,
                        type=type,
                        polygon=poly)
            plot.save()
        else:
            print("floor e asche")
            plot_code = Plot.objects.get(plot_id=int(total[1]), area_id=Area.objects.get(pk=int(total[0])))
            description = total[2]
            type = total[3]
            floor_id = total[4]

            public = Public(plot_code=plot_code,
                            floor_id=floor_id,
                            name=name,
                            description=description,
                            lat=latitude,
                            lng=longitude,
                            alt=altitude,
                            type=type,
                            polygon=poly)
            public.save()


    return HttpResponse(data)
