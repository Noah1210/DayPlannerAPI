from django.http import JsonResponse


def create_response(message, status=200, data=None):
    response_data = {'message': message}
    if data is not None:
        response_data.update(data)
    return JsonResponse(response_data, status=status)

def create_error(message, status=400):
    response_data = {'error': message}
    return JsonResponse(response_data, status=status)
