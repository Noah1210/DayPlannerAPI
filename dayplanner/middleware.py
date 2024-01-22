from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the token from the request
        token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        token = Token.objects.filter(key=token_key).first()

        # If the token exists and is about to expire, return an error response
        if token and token.expires - timezone.now() < timezone.timedelta(minutes=30):
            return JsonResponse({'error': 'Token is about to expire. Please refresh the token.'}, status=401)

        # Otherwise, continue processing the request
        return self.get_response(request)