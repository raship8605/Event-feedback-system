from django.contrib import admin
from .models import Event, Attendee, Feedback
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=['id','name','date','average_rating','created_at']
    list_filter=['date','created_at']
    search_fields=['name']

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display=['id','name','email']
    search_fields=['name','email']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'attendee', 'rating', 'created_at']
    list_filter=['rating','event']
    search_fields=['comment']
