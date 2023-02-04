
from django.urls import path,include
from .views import login
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',login,name="login")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
