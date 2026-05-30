from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Attendee, Feedback
from .serializers import EventSerializer, AttendeeSerializer, FeedbackSerializer

#Event Views

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def event_list_create(request):
    if request.method=='GET':  #read
        events=Event.objects.all()
        serializer=EventSerializer(events, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, pk):
    try:
        event=Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error':'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=EventSerializer(event)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer.EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# feedback views
@api_view(['GET','POST'])
@permission_classes([AllowAny])  #anyone can give feedback
def feedback_list_create(request, event_id=None):
    if request.method=='GET':
        if event_id:
            feedbacks=Feedback.objects.filter(event_id=event_id)
        else:
            feedbacks=Feedback.objects.all()
        serializer=FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        # create or get attendee
        attendee_email=request.data.get('attendee_email')
        attendee_name=request.data.get('attendee_name')

        if not attendee_email or not attendee_name:
            return Response({'error':'attendee email and attendee name required'}, status=status.HTTP_400_BAD_REQUEST)
        attendee, created=Attendee.objects.get_or_create(
            email=attendee_email,
            defaults={'name':attendee_name}
        )
        data={
            'event':event_id,
            'attendee':attendee.id,
            'rating':request.data.get('rating'),
            'comment':request.data.get('comment', '')
        }
        serializer=FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Analytics view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_analytics(request, event_id):
    try:
        event=Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response({'error':'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    feedbacks=event.feedbacks.all()
    total=feedbacks.count()

    if total==0:
        return Response({'message':'Not feedback ye','event_name':event.name})
    rating_distribution={
        1:feedbacks.filter(rating=1).count(),
        2:feedbacks.filter(rating=2).count(),
        3:feedbacks.filter(rating=3).count(),
        4:feedbacks.filter(rating=4).count(),
        5:feedbacks.filter(rating=5).count(),
    }
    return Response({
        'event_name':event.name,
        'total_feedbacks':total,
        'average_rating':round(event.average_rating, 2),
        'rating_distribution':rating_distribution,
        'recent_comments':FeedbackSerializer(feedbacks.order_by('-created_at')[:5],many=True).data
    })




