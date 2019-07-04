from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserView)
router.register('todolists', views.TodoView)
router.register('orglists', views.OrganizationView)

app_name = 'todo'
urlpatterns = [
    path('', include(router.urls)),
]