from django.shortcuts import render,redirect

# Create your views here.
import subprocess
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        if 'ssid' in request.POST and 'password' in request.POST:
            ssid = request.POST['ssid']
            password = request.POST['password']

            conf = 'network={\n' \
                   '    ssid="' + ssid + '"\n' \
                   '    psk="' + password + '"\n' \
                   '}\n'

            with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
                f.write(conf)

            output = subprocess.call(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'], shell=True)
            if output == 0:
                return HttpResponse("Wifi Connected")
            else:
                return HttpResponse("Failed to connect to wifi")
        else:
            return HttpResponse("Missing ssid or password")
    return render(request, 'login.html')