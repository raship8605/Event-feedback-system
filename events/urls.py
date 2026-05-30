from django.urls import path
from .import views

urlpattens=[
     path('event_list/',views.event_list_create, name='event_list'),
     path('events/<int:pk>/',views.event_detail, name='event_details')
]