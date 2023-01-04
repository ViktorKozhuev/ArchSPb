from django.urls import path

from .views import *


urlpatterns = [
    path('', BuildingsHome.as_view(), name='home'),
    path('architects/', Architects.as_view(), name='architects'),
    path('archstyle/', ArchStyles.as_view(), name='archstyles'),
    path('streets/', Streets.as_view(), name='streets'),
    path('<slug:slug>/', ShowBuilding.as_view(), name='building_detail'),

    path('archstyle/<slug:slug>/', BuildingsArchStyle.as_view(), name='archstyle'),
    path('architect/<slug:slug>/', BuildingsArchitect.as_view(), name='architect'),
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('street/<slug:slug>/', BuildingsStreet.as_view(), name='street'),
    path('category/<slug:category_url>/', BuildingsCategory.as_view(), name='category'),

    # path('<slug:slug>/', ShowBuilding.as_view(), name='building'),


    ]
