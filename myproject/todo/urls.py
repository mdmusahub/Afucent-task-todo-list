from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',Logout.as_view()),
    path('todo/',TodoApiView.as_view()),
]