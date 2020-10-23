from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from account import views

app_name = "users"

urlpatterns = [
    path('', csrf_exempt(views.UserListCreateView.as_view())),
    path('<pk>/', views.UserDetails.as_view()),
]