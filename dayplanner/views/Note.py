from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from dayplanner.bearerTokenAuth import BearerTokenAuthentication
from dayplanner.models import Note
from dayplanner.serializers import NoteSerializer
from dayplanner.utils.api_responses import create_response, create_error


class NoteView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print("request : ", request.GET.get('date'))
        date = request.GET.get('date')
        if date:
            notes = Note.objects.extra(where=["DATE(date) = %s"], params=[date])
        else:
            notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return create_response('Notes retrieved successfully', status.HTTP_200_OK, {'response': serializer.data})

    def post(self, request):
        print("request : ", request.data)
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response('Note created successfully', status.HTTP_201_CREATED, serializer.data)
        return create_error('Invalid note data', status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return create_response('Note updated successfully', status.HTTP_200_OK, serializer.data)
        return create_error('Invalid note data', status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        return create_response('Note deleted successfully', status.HTTP_200_OK)