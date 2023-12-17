from django.contrib.auth.models import User
from rest_framework import serializers

from dayplanner.models import Note, Task, Todo


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Note
        fields = ['content', 'date', 'user']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'date_start', 'date_end', 'color', 'user']


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'date', 'is_done', 'is_priority', 'user']
