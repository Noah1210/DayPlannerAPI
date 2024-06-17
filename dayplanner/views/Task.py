from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from dayplanner.bearerTokenAuth import BearerTokenAuthentication
from dayplanner.models import Todo
from dayplanner.serializers import TaskSerializer
from dayplanner.utils.api_responses import create_response, create_error


class TaskView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print("request : ", request.GET.get('date'))
        date = request.GET.get('date')
        if date:
            tasks = Todo.objects.extra(where=["DATE(date) = %s"], params=[date])
        else:
            tasks = Todo.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return create_response('Tasks retrieved successfully', status.HTTP_200_OK, {'response': serializer.data})

    def post(self, request):
        print("request : ", request.data)
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response('Task created successfully', status.HTTP_201_CREATED, serializer.data)
        return create_error('Invalid task data', status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = Todo.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return create_response('Task updated successfully', status.HTTP_200_OK, serializer.data)
        return create_error('Invalid task data', status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = Todo.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return create_response('Task updated successfully', status.HTTP_200_OK, serializer.data)
        return create_error('Invalid task data', status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = Todo.objects.get(pk=pk)
        task.delete()
        return create_response('Task deleted successfully', status.HTTP_200_OK)