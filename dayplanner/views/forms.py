from django import forms
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginThrottle(AnonRateThrottle):
    rate = '10/hour'


def require_post(view_func):
    @csrf_exempt
    @method_decorator(throttle_classes([LoginThrottle]))
    def _decorator(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        return view_func(request, *args, **kwargs)

    return _decorator


def require_get(view_func):
    @csrf_exempt
    @method_decorator(throttle_classes([LoginThrottle]))
    def _decorator(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        return view_func(request, *args, **kwargs)

    return _decorator
