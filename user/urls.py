from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_jwt import views as jwt


router = SimpleRouter()

router.register('register', views.UserList, 'register')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^login/$', views.Login, name='Login'),
    url(r'^logout/$', views.Logout, name='Logout'),
    url(r'^api/token/refresh/$', jwt.refresh_jwt_token),
    url(r'^api/token/verify/$', jwt.verify_jwt_token),
    url(r'^api/token/$', jwt.obtain_jwt_token),
    url(r'^upkml/$', views.upkml, name='upkml'),
    url(r'^check/(?P<plot_id>[0-9]+)/$', views.check_plot, name='check_plot'),
    url(r'^plot/$', views.PlotView.as_view(), name='plot'),
    url(r'^plot/detail/(?P<plot_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^plot/update_plot/(?P<plot_id>[0-9]+)/$', views.update_plot, name='update_plot'),
    url(r'^plot/(?P<plot_id>[0-9]+)/$', views.public, name='public'),
    url(r'^plot/([0-9]+)/detail/(?P<id>[0-9]+)/$', views.detail_public, name='public_detail'),
    url(r'^plot/([0-9]+)/update_public/(?P<id>[0-9]+)/$', views.update_public, name='update_public'),
    url(r'^check_public/(?P<id>[0-9]+)/$', views.check_public, name='check_public'),
    url(r'^create_poi/$', views.create_poi, name='create_poi'),
    url(r'^create_poi/open_kml/$', views.create_poi_kml, name='create_poi_kml'),
    url(r'^create_poi_form/$', views.create_poi_form, name='create_poi_form'),
    url(r'^create_floor_form/$', views.create_floor_form, name='create_floor_form'),
    url(r'^create_poi/validate/$', views.create_poi_validate, name='create_poi_validate'),
    url(r'^add_poi/$', views.add_poi, name='add_poi'),
    url(r'^add_poi/validate/$', views.add_poi_validate, name='add_poi_validate'),
]


