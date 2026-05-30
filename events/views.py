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
    

