
from django.urls import path,include
from .views import login,reading_data
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',login,name="login"),
    path('reading_data',reading_data,name="reading_data")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
