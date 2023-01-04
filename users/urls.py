from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'users'

urlpatterns = [
    path(
        route='login',
        view=LoginView.as_view(),
        name='login'
    ),
    path(
        route='register',
        view=SignupView.as_view(),
        name='register'
    ),
    path(
        route='logout/',
        view=LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='register_completed/',
        view=TemplateView.as_view(template_name='users/registerok.html'),
        name='registerok'
    ),

    path(
        route='profile',
        view=profile,
        name='profile'
    ),
]
