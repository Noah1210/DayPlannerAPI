from django.urls import path
from rest_framework.routers import DefaultRouter

from dayplanner.views import NoteViewSet
from dayplanner.views.Event import EventView
from dayplanner.views.Task import TaskView
from dayplanner.views.auth_views import RefreshTokenView, registration_view, logout_view, loginView

urlpatterns = [
    path('login/', loginView.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('event/', EventView.as_view(), name='event-all'),
    path('event/<int:pk>', EventView.as_view(), name='event-specific'),
    path('task/', TaskView.as_view(), name='task-all'),
    path('task/<int:pk>', TaskView.as_view(), name='task-specific'),
]
