import datetime

from rest_framework import viewsets, permissions

from dayplanner.models import Note
from dayplanner.serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Note.objects.filter(user=user, date=datetime.date.today())


        return queryset