from django.conf.urls import url, include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_jwt import views as jwt


router = SimpleRouter()

router.register('people', views.PeopleList, 'people')
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

]


