from django.urls import path
from .import views

urlpattens=[
    #event url
    path('event_list/',views.event_list_create, name='event_list'),
    path('events/<int:pk>/',views.event_detail, name='event_details'),

    #Feedback Url
    path('events/<int:event_id>/feedback/', views.feedback_list_create, name='feedback-list'),
    path('feedback/',views.feedback_list_create, name='all-feedback'),

    #Analytics url
    path('events/<int:event_id/analytics/',views.event_analytics,name='analytics'),
    
]