import datetime

from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import date
from dayplanner.bearerTokenAuth import BearerTokenAuthentication
from dayplanner.models import Task
from dayplanner.serializers import EventSerializer
from dayplanner.utils.api_responses import create_response, create_error


class EventView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print("request : ", request.GET.get('date'))
        date = request.GET.get('date')
        if date:
            events = Task.objects.extra(where=["DATE(date_start) = %s"], params=[date])
        else:
            events = Task.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})
        return create_response('events retrieved successfully', status.HTTP_200_OK, {'response': serializer.data})

    def post(self, request):
        #TODO Make sure an event can only last for 24 hours (on create, and update)
        print("request : ", request.data)
        #verify_event_less_than_24_hours(request.data.get('date_start'), request.data.get('date_end'))
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response('Event created successfully', status.HTTP_201_CREATED, serializer.data)
        return create_error('Invalid event data', status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event = Task.objects.get(pk=pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return create_response('event updated successfully', status.HTTP_200_OK, serializer.data)
        return create_error('Invalid event data', status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = Task.objects.get(pk=pk)
        event.delete()
        return create_response('event deleted successfully', status.HTTP_200_OK)


def verify_event_less_than_24_hours(date_start, date_end):
    #I can't use the time I need to make sure the event i on the same date
    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
    date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")
    difference = date_end - date_start
    print(f"difference :  {difference} date_start : {date_start}")
    if difference.days > 0 or difference.seconds >= 86400:  # 24 hours
        print("Event is more than 24 hours")
        return False
    print("Event is less than 24 hours")
    return True
