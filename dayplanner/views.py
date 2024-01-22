import datetime

from django import forms
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import throttle_classes

from dayplanner.models import Note, User
from dayplanner.serializers import NoteSerializer


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginThrottle(AnonRateThrottle):
    rate = '10/hour'


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


@csrf_exempt
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already in use'}, status=400)
            else:
                user = User.objects.create_user(username, email, password)
                if user is not None:
                    login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                    return JsonResponse({'message': 'Registration successful', 'token': token.key}, status=201)
                else:
                    return JsonResponse({'error': 'Unable to create user'}, status=400)
        else:
            return JsonResponse({'error': 'Username, email, and password are required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@throttle_classes([LoginThrottle])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'Login successful', 'token': token.key}, status=200)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=401)
        else:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def logout_view(request):
    if request.method == 'POST':
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class RefreshTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if token.expires > timezone.now():
            token.expires = timezone.now() + timezone.timedelta(hours=2)
            token.save()

            return Response({'token': token.key, 'expires': token.expires})

        return Response({'detail': 'Token has expired. Please log in again.'}, status=401)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user

        queryset = Note.objects.filter(user=user, date=datetime.date.today())

        return queryset
