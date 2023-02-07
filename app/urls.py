
from django.urls import path,include
from .views import login,reading_data,treatment_running,wifi_names
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',login,name="login"),
    path('reading_data',reading_data,name="reading_data"),
    path('treatment_running',treatment_running,name="treatment_running"),
    path('wifi_names',wifi_names,name="wifi_names"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
