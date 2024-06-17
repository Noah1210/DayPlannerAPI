
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from dayplanner.models import Note, Task, Todo, User


class RefreshTokenSerializer(serializers.Serializer):

    def validate(self, attrs):
        request = self.context.get('request')
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header or 'Bearer' not in auth_header:
            msg = 'Auth error.'
            raise serializers.ValidationError(msg, code='authorization')

        auth_parts = auth_header.split(' ')
        if len(auth_parts) < 2:
            msg = 'Token is missing.'
            raise serializers.ValidationError(msg, code='authorization')

        token = auth_parts[1]

        if not token:
            msg = 'Token is required.'
            raise serializers.ValidationError(msg, code='authorization')

        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            msg = 'Invalid token.'
            raise serializers.ValidationError(msg, code='authorization')

        if not token_obj.user.is_active:
            msg = 'User inactive or deleted.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = token_obj.user
        return attrs


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ['content', 'date', 'user']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'date_start', 'date_end', 'color']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'date', 'is_done', 'is_priority']
