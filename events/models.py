from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    name=models.CharField(max_length=200)
    date=models.DateTimeField()
    description=models.TextField(blank=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        ratings=self.feedbacks.filter(rating_isnull=False)
        if ratings:
            return sum(f.rating for f in ratings)/len(ratings)
        return 0
    
class Attendee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    attendee=models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='feedbacks')
    rating=models.IntegerField(choices=[(i, i) for i in range(1,6)])
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=['event','attendee']  #one feedback per person per event only

        def __str__(self):
            return f"{self.attendee.name}- {self.event.name}- {self.rating} ★"




