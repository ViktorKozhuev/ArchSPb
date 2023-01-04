from django.urls import path

from .views import *

app_name = 'posts'

urlpatterns = [
    path('', Posts.as_view(), name='index'),
    path('add_post/', add_post, name='add_post'),
    path('<slug:url>/', ShowPost.as_view(), name='post'),
    path('comment/<int:pk>/', add_comment, name='add_comment'),

    ]
