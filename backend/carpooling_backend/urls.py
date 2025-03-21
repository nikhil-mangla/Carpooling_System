
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Carpooling Backend API! Try /api/rides/ for ride data.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rides.urls')),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),  
]