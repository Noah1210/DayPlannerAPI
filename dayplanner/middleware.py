from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.http import JsonResponse


class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the token from the request
        print(request.path)
        auth = ['/api/login/', '/api/register/', '/api/logout/', '/api/refresh-token/']
        # TODO: No path verification
        # if request.path not in auth:
        #     token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        #     token = Token.objects.filter(key=token_key).first()
        #
        #     # If the token exists and has expired, return an error response
        #     if request.user.is_authenticated:
        #         token = Token.objects.filter(user=request.user).first()
        #         print(token.created)
        #         if token and timezone.now() > token.created + timezone.timedelta(hours=3):
        #             return JsonResponse({'detail': 'Token has expired. Please log in again.'}, status=401)
        #
        #     # If the token exists and is about to expire, return an error response
        #     if token and timezone.now() > token.created + timezone.timedelta(hours=2):
        #         return JsonResponse({'detail': 'Token is about to expire. Please refresh the token.'}, status=401)

        return self.get_response(request)
