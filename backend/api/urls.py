from django.urls import path
from .views import home, test, detect

urlpatterns = [
    path('', home),
    path('test/', test),
    path('detect/', detect),
]