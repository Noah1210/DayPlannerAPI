from datetime import timedelta

from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dayplanner.models import User
from dayplanner.serializers import RefreshTokenSerializer
from dayplanner.utils.api_responses import create_error, create_response
from dayplanner.views.forms import require_post, RegistrationForm, LoginForm


@require_post
def registration_view(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if User.objects.filter(email=email).exists():
            return create_error('Email already in use', status=400)
        else:
            try:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                creation_timestamp = int(token.created.timestamp() * 1000)

                return create_response('Registration successful', 201,
                                       {'token': token.key, 'creation_date': creation_timestamp})
            except Exception as e:
                return create_error('Unable to create user: ' + str(e), status=400)

    else:
        return create_error('Username, email, and password are required', status=400)


class loginView(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if request.user.is_authenticated:
            print('User is already logged in')
            Token.objects.filter(user=request.user).delete()
            logout(request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                token = create_new_token_if_expired(token, user)
                print(f"created :  {token.created}")
                creation_timestamp = int(token.created.timestamp() * 1000)
                print(f"milisec :  {creation_timestamp}")
                print(request.user.is_authenticated)
                return create_response('Login successful', 200,
                                       {'token': token.key, 'creation_date': creation_timestamp})
            else:
                return create_error('Invalid email or password', status=401)
        else:
            return create_error('Invalid form', status=401)


@require_post
def logout_view(request):
    if request.user.is_authenticated:
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return create_response('Logout successful', 200)
        except Exception as e:
            return create_error('Logout unsuccessful: ' + str(e), 500)
    else:
        return create_error('Logout unsuccessful: No user is currently logged in', 401)


class RefreshTokenView(ObtainAuthToken):
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        token_lifetime = timedelta(hours=3)
        token_hard_limit = timedelta(hours=24)

        if created or timezone.now() - token.created < token_hard_limit:
            if timezone.now() - token.created < token_lifetime:
                token.created = timezone.now()
                token.save()
                creation_timestamp = int(token.created.timestamp() * 1000)
                return Response({'token': token.key, 'creation_date': creation_timestamp})
        return Response({'detail': 'Token has expired. Please log in again.'}, status=401)


def create_new_token_if_expired(token, user):
    if timezone.now() > token.created + timedelta(hours=3):
        token.delete()
        token = Token.objects.create(user=user)
    return token