from rest_framework import serializers
from .models import Event, Attendee, Feedback

class EventSerializer(serializers.ModelSerializers):
    average_rating=serializers.ReadOnlyField()
    total_feedbacks=serializers.SerializerMethodField()

    class Meta:
        model=Event
        fields=['id','name','date','description','created_by','average_rating','total_feedbacks','created_at']
        read_only_fields=['created_by','created_at']

    def get_total_feedbacks(self,obj):
        return obj.feedbacks.count()
    
class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendee
        fields=['id','name','email']

class FeedbackSerializer(serializers.ModelSerializer):
    attendee_name=serializers.ReadOnlyField(source='attendee.name')

    class Meta:
        model=Feedback
        fields=['id','event','event_name','attendee','attendee_name','rating','comment','created_at']
        read_only_fields=['created_at']

