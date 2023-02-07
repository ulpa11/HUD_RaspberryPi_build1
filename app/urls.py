#import path
from django.urls import path
from .views import wifi_names, login, reading_data,treatment_running

urlpatterns = [
    path('', wifi_names, name='wifi_names'),
    path('login/', login, name='login'),
    path('reading_data/', reading_data, name='reading_data'),
    path('treatment_running/', treatment_running, name='treatment_running'),
]