from django.contrib import admin
from django.urls import path, include

from account import views

app_name = "project"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', views.UserAuth.as_view()),
    path('users/', include('account.urls')),
    path('groups/', views.GroupList.as_view()),
    path('clients/', views.ClientCreateView.as_view(), name='create_client'),
]
