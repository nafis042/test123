from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('people', views.PeopleList, 'people')
router.register('register', views.UserList, 'register')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^login/$', views.Login, name='Login'),
    url(r'^logout/$', views.Logout, name='Logout'),

]


