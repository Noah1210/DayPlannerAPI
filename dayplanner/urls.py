from django.urls import path
from .views import login_view, RefreshTokenView, registration_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', login_view, name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    # Include other app URLs as needed
]