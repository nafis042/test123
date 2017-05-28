from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from user.forms import RegistrationForm, LoginForm, UploadForm, UpdateForm, UpdatePOIForm, UpdatePublicForm, \
    UpdateFloorForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Plot, Public, Area, POI, Floor
from . import serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from fastkml import kml
from shapely.geometry import Point, Polygon
from django.views import generic
from pathlib import Path
import os


def index(request):
    return render(request, "base.html")


def upkml(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            uploaded_files = request.FILES['file']
            print(uploaded_files.name)
            temp = uploaded_files.name.split('_')
            path = 'Bangladesh/' + temp[0] + '/' + temp[1]
            os.makedirs(path, exist_ok=True)
            path += '/' + uploaded_files.name
            with open(path, 'wb+') as destination:
                for chunk in uploaded_files.chunks():
                    destination.write(chunk)
            parse(request, path)
       # return render(request, "base.html")
        return redirect('/user')
    else:
        form = UploadForm()
        return render(request, "upkml.html", {'form': form})


def update_plot(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    return render(request, "update.html", {'plot': plot})


def check_plot(request, plot_id):
    print("asche")
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            print("asche")
            t = Plot.objects.get(id=plot_id)
            t.area_id = form.cleaned_data['area_id']
            t.plot_id = form.cleaned_data['plot_id']
            t.lat = form.cleaned_data['lat']
            t.lng = form.cleaned_data['lng']
            t.alt = form.cleaned_data['alt']
            t.name = form.cleaned_data['name']
            t.description = form.cleaned_data['description']
            t.type = form.cleaned_data['type']
            t.polygon = form.cleaned_data['polygon']
            t.save()
            area = str(form.cleaned_data['area_id'])
            plot = str(form.cleaned_data['plot_id'])
            path = 'Bangladesh' + '/' + '1' + '/' + area + '/' + '1_' + area + '_' + plot + '.kml'
            print(path)
            file = Path(path)
            if file.exists():
                os.remove(path)
            k = kml.KML()
            ns = '{http://www.opengis.net/kml/2.2}'
            d = kml.Document(ns, 'docid', 'docname', 'docdesc')
            k.append(d)
            desc = area + ' ' + plot + ' ' + form.cleaned_data['description'] + ' ' + form.cleaned_data['type']
            p = kml.Placemark(ns, 'id', form.cleaned_data['name'], desc)
            list = []
            print('full data')
            print(form.cleaned_data['polygon'])
            if 'NULL' in form.cleaned_data['polygon']:
                p.geometry = Point(float(form.cleaned_data['lat']), float(form.cleaned_data['lng']), float(form.cleaned_data['alt']))
            else:
                temp = form.cleaned_data['polygon']
                temp = temp.replace(', ', ',')
                temp1 = temp.split(',')
                for i in temp1:
                    strr = i
                    str1 = strr.split(' ')
                    print(str1)
                    list_temp = []
                    list_temp.append(float(str1[0]))
                    list_temp.append(float(str1[1]))
                    list_temp.append(float(str1[2]))
                    list.append(list_temp)
                    print(list)
                p.geometry = Polygon(list)
            d.append(p)
            out = open(path, 'w+')
            final = k.to_string(prettyprint=True)
            out.write(final)
            out.close()
            print(k.to_string(prettyprint=True))
        else:
            print(form.errors)
    return redirect('/user')


def registration(request):
        if request.user.is_authenticated():
            return HttpResponse("Already In")
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                User.objects.create_user(username=form.cleaned_data['first_name'],
                                         email=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'],
                                         first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleaned_data['last_name'],
                                         )
                return HttpResponseRedirect('/user/login')
            else:
                return render(request, "register.html", {'form': form})

        else:
            ''' user is not submitting the form, show them a blank registration form '''
            form = RegistrationForm()
            return render(request, "register.html", {'form': form})


def Login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/')
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


@permission_classes([IsAuthenticated])
class UserList(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_create(self, serializer):
        # serializer.validated_data.update({'company_id': get_company_id(self.request)})
        super().perform_create(serializer)

    def get_queryset(self):
        return super().get_queryset()


def parse(request,path):
    with open(path, 'r') as myfile:
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
            temp = temp.replace("POINT Z (", "").replace(")", "")
            temp1 = temp.split()
            latitude = temp1[0]
            longitude = temp1[1]
            altitude = temp1[2]
            poly = "NULL"
            print(latitude+" "+longitude+" "+altitude)
        else:
            poly = str(i.geometry).replace("POLYGON((", "").replace("))", "")
            poly = poly.replace("POLYGON Z ((", "").replace("))", "")
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


class PlotView(generic.ListView):
    template_name = 'plot.html'

    def get_queryset(self):
        return Plot.objects.all()


def public(request, plot_id):
    queryset = Public.objects.filter(plot_code=plot_id)
    plot = get_object_or_404(Plot, pk=plot_id)
    return render(request, 'public.html', {'Pub': queryset, 'name': plot.name})


def detail_public(request, id):
    pub = get_object_or_404(Public, pk=id)
    return render(request, 'detail_public.html', {'public': pub})


def detail(request, plot_id):
        plot = get_object_or_404(Plot, pk=plot_id)
        return render(request, 'detail.html', {'plot': plot})


def update_public(request, id):
    pub = get_object_or_404(Public, pk=id)
    return render(request, "update_public.html", {'public': pub})


def check_public(request, id):
    if request.method == 'POST':
        form = UpdatePublicForm(request.POST)
        if form.is_valid():
            print("asche")
            t = Public.objects.get(pk=id)
            t.area_id = form.cleaned_data['plot_code']
            t.plot_id = form.cleaned_data['floor_id']
            t.lat = form.cleaned_data['lat']
            t.lng = form.cleaned_data['lng']
            t.alt = form.cleaned_data['alt']
            t.name = form.cleaned_data['name']
            t.description = form.cleaned_data['description']
            t.type = form.cleaned_data['type']
            t.polygon = form.cleaned_data['polygon']
            t.save()
            plott = Plot.objects.get(plot_id=t.plot_code.plot_id)
            area = str(plott.area_id.pk)
            plot = str(form.cleaned_data['plot_code'])
            path = 'Bangladesh' + '/' + '1' + '/' + area + '/' + plot + '/' + '1_' + area + '_' + plot + '_' + id + '.kml'
            directory = 'Bangladesh' + '/' + '1' + '/' + area + '/' + plot
            print(path)
            file = Path(path)
            if file.exists():
                os.remove(path)
            else:
                os.makedirs(directory, exist_ok=True)
            k = kml.KML()
            ns = '{http://www.opengis.net/kml/2.2}'
            d = kml.Document(ns, 'docid', 'docname', 'docdesc')
            k.append(d)
            desc = area + ' ' + plot + ' ' + form.cleaned_data['description'] + ' ' + form.cleaned_data['type'] + ' ' + str(form.cleaned_data['floor_id'])
            p = kml.Placemark(ns, 'id', form.cleaned_data['name'], desc)
            list = []
            print('full data')
            print(form.cleaned_data['polygon'])
            if 'NULL' in form.cleaned_data['polygon']:
                p.geometry = Point(float(form.cleaned_data['lat']), float(form.cleaned_data['lng']), float(form.cleaned_data['alt']))
            else:
                temp = form.cleaned_data['polygon']
                temp = temp.replace(', ', ',')
                temp1 = temp.split(',')
                for i in temp1:
                    strr = i
                    str1 = strr.split(' ')
                    print(str1)
                    list_temp = []
                    list_temp.append(float(str1[0]))
                    list_temp.append(float(str1[1]))
                    list_temp.append(float(str1[2]))
                    list.append(list_temp)
                    print(list)
                p.geometry = Polygon(list)
            d.append(p)
            out = open(path, 'w')
            final = k.to_string(prettyprint=True)
            out.write(final)
            out.close()
            print(k.to_string(prettyprint=True))
        else:
            print(form.errors)
    return redirect('/user')


def write_poi_to_floor(area_id, plot_id, floor_id, poi_id):
    area_id = str(area_id)
    plot_id = str(plot_id)
    floor_id = str(floor_id)
    poi_id = str(poi_id)
    path = 'Bangladesh' + '/' + '1' + '/' + area_id + '/' + plot_id + '/' + '1_' + area_id + '_' + plot_id + \
           '_' + floor_id + '.kml'
    print(path)
    with open(path, 'r') as file:
        data = file.read()
    poi = POI.objects.get(pk=poi_id)
    ns = '{http://www.opengis.net/kml/2.2}'
    k = kml.KML()
    k.from_string(data)
    features = list(k.features())
    print(len(features))
    p = kml.Placemark(ns, "new", poi.name, poi.description)
    li = []
    print('full data')
    print(poi.polygon)
    if len(poi.polygon) < 5:
        p.geometry = Point(float(poi.lat), float(poi.lng),
                           float(poi.alt))
    else:
        temp = poi.polygon
        temp = temp.replace(', ', ',')
        temp1 = temp.split(',')
        for i in temp1:
            strr = i
            str1 = strr.split(' ')
            print(str1)
            list_temp = []
            list_temp.append(float(str1[0]))
            list_temp.append(float(str1[1]))
            list_temp.append(float(str1[2]))
            li.append(list_temp)
            print(li)
        p.geometry = Polygon(li)

    placemark_list = list(features[0].features())
    placemark_list.append(p)
    print(len(placemark_list))
    file = Path(path)
    if file.exists():
        os.remove(path)
    k = kml.KML()
    d = kml.Document(ns, features[0].id, features[0].name, features[0].description)
    k.append(d)
    for placemark in placemark_list:
        p = kml.Placemark(ns, placemark.id, placemark.name, placemark.description)
        p.geometry = placemark.geometry
        d.append(p)
    out = open(path, 'w+')
    final = k.to_string(prettyprint=True)
    out.write(final)
    out.close()

    return HttpResponse(final)


def create_poi(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            uploaded_files = request.FILES['file']
            print(uploaded_files.name)
            path = 'media/' + uploaded_files.name
            print(path)
            with open(path, 'r') as myfile:
                data = myfile.read()
            print(data)
            file = Path(path)
            if file.exists():
                os.remove(path)
            k = kml.KML()
            k.from_string(data)
            features = list(k.features())
            f2 = list(features[0].features())
            print(len(f2))
            if len(f2) > 1:
                form = UploadForm()
                poi = POI.objects.filter(assigned=False, uploader=request.user)
                return render(request, "create_poi.html",
                              {"form": form, "Poi": poi, "error": "Please select a valid kml file"})
            else:

                print(f2[0].name + " " + f2[0].description + " " + str(f2[0].geometry))

                if "POINT" in str(f2[0].geometry):
                    # print("asche")
                    temp = str(f2[0].geometry).replace("POINT (", "").replace(")", "")
                    temp = temp.replace("POINT Z (", "").replace(")", "")
                    temp1 = temp.split()
                    latitude = temp1[0]
                    longitude = temp1[1]
                    altitude = temp1[2]
                    poly = "NULL"
                    print(latitude + " " + longitude + " " + altitude)
                else:
                    poly = str(f2[0].geometry).replace("POLYGON((", "").replace("))", "")
                    poly = poly.replace("POLYGON Z ((", "").replace("))", "")
                    latitude = "NULL"
                    longitude = "NULL"
                    altitude = "NULL"
                    print(poly)

                name = str(f2[0].name)
                form = UploadForm()
                poi = POI.objects.filter(assigned=False, uploader=request.user)
                return render(request, "create_poi.html",
                              {"form": form, "Poi": poi, "name": name, "lat": latitude, "lan": longitude,
                               "alt": altitude, "poly": poly})
    else:
        form = UploadForm()
        poi = POI.objects.filter(assigned=False, uploader=request.user)
        return render(request, "create_poi.html", {"form": form, "Poi": poi})


def create_poi_kml(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            uploaded_files = request.FILES['file']
            print(uploaded_files.name)
            path = 'media/' + uploaded_files.name
            print(path)
            with open(path, 'r') as myfile:
                data = myfile.read()
            print(data)
            file = Path(path)
            if file.exists():
                os.remove(path)
            k = kml.KML()
            k.from_string(data)
            features = list(k.features())
            f2 = list(features[0].features())
            print(len(f2))
            if len(f2) > 1:
                form = UploadForm()
                poi = POI.objects.filter(assigned=False, uploader=request.user)
                return render(request, "create_poi.html", {"form": form, "Poi": poi, "error": "Please select a valid kml file"})
            else:

                print(f2[0].name + " " + f2[0].description + " " + str(f2[0].geometry))

                if "POINT" in str(f2[0].geometry):
                    # print("asche")
                    temp = str(f2[0].geometry).replace("POINT (", "").replace(")", "")
                    temp = temp.replace("POINT Z (", "").replace(")", "")
                    temp1 = temp.split()
                    latitude = temp1[0]
                    longitude = temp1[1]
                    altitude = temp1[2]
                    poly = "NULL"
                    print(latitude + " " + longitude + " " + altitude)
                else:
                    poly = str(f2[0].geometry).replace("POLYGON((", "").replace("))", "")
                    poly = poly.replace("POLYGON Z ((", "").replace("))", "")
                    latitude = "NULL"
                    longitude = "NULL"
                    altitude = "NULL"
                    print(poly)

                name = str(f2[0].name)
                form = UploadForm()
                poi = POI.objects.filter(assigned=False, uploader=request.user)
                return render(request, "create_poi.html", {"form": form, "Poi": poi, "name": name, "lat": latitude, "lan": longitude,
                                                           "alt": altitude, "poly": poly})


def create_poi_validate(request):
    print("asche")
    poi_id = request.GET.get('poi')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    alt = request.GET.get('alt')
    poly = request.GET.get('poly')
    print(lat + " " + lng + " " + alt + " " + poly)
    print(poi_id)
    poi = POI.objects.get(pk=poi_id)
    poi.lat = lat
    poi.lng = lng
    poi.alt = alt
    poi.polygon = poly
    poi.save()
    data = {
        'success': "success"
    }
    return JsonResponse(data)


def create_poi_form(request):
    if request.method == 'POST':
        print("asche")
        form = UpdatePOIForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(request.user)
            poi = POI(uploader=request.user,
                      floor_id=form.cleaned_data['floor_id'],
                      name=form.cleaned_data['name'],
                      description=form.cleaned_data['description'],
                      webaddress=form.cleaned_data['webaddress'],
                      mobile=form.cleaned_data['mobile'],
                      lat=form.cleaned_data['lat'],
                      lng=form.cleaned_data['lng'],
                      alt=form.cleaned_data['alt'],
                      type=form.cleaned_data['type'],
                      polygon=form.cleaned_data['polygon'])
            poi.save()
            return HttpResponseRedirect('/user')
    else:
        form = UpdatePOIForm()
        return render(request, "create_poi_form.html", {'form': form})


def create_floor_form(request):
    if request.method == 'POST':
        print("asche")
        form = UpdateFloorForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(request.user)
            floor = Floor(plot_id=form.cleaned_data['plot_id'],
                          floor_id=form.cleaned_data['floor_id'],
                          description=form.cleaned_data['description'])
            floor.save()
            plott = Plot.objects.get(pk=str(form.cleaned_data['plot_id']))
            area = str(plott.area_id.pk)
            plot = str(form.cleaned_data['plot_id'])
            path = 'Bangladesh' + '/' + '1' + '/' + area + '/' + plot + '/' + \
                   '1_' + area + '_' + plot + '_' + str(floor.pk) + '.kml'
            directory = 'Bangladesh' + '/' + '1' + '/' + area + '/' + plot
            print(path)
            file = Path(path)
            if file.exists():
                os.remove(path)
            else:
                os.makedirs(directory, exist_ok=True)
            k = kml.KML()
            ns = '{http://www.opengis.net/kml/2.2}'
            d = kml.Document(ns, floor.pk, 'docname', floor.description)
            k.append(d)
            out = open(path, 'w')
            final = k.to_string(prettyprint=True)
            out.write(final)
            out.close()

            return HttpResponseRedirect('/user')
    else:
        form = UpdateFloorForm()
        return render(request, "create_floor_form.html", {'form': form})


def add_poi(request):
    floor = Floor.objects.all()
    poi = POI.objects.filter(assigned=False, uploader=request.user)
    return render(request, "add_poi.html", {"floor": floor, "Poi": poi})


def add_poi_validate(request):
    print("asche")
    poi_id = request.GET.get('poi')
    floor_id = request.GET.get('floor')
    floor_id = int(floor_id)
    floor = Floor.objects.get(pk=floor_id)
    plot = Plot.objects.get(pk=str(floor.plot_id))
    area = plot.area_id
    print(poi_id)
    print(str(area) + " " + str(floor.plot_id) + " " + str(floor_id))
    total = poi_id.split(' ')
    for i in total:
        id = int(i)
        poi = POI.objects.get(pk=id)
        poi.floor_info = floor
        poi.assigned = True
        poi.save()
        write_poi_to_floor(area, floor.plot_id, floor_id, id)


    data = {
        'success': "success"
    }
    return JsonResponse(data)


def test(request):
    return render(request, "test.html")