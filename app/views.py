from django.shortcuts import render, redirect
import subprocess
import sys

# Create your views here.
import subprocess
from django.http import HttpResponse


def login(request):
    if request.method == 'POST':
        if 'ssid' in request.POST and 'password' in request.POST:
            ssid = request.POST['ssid']
            password = request.POST['password']
            wpa_supplicant_conf = f"""
                country=US
                ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
                update_config=1
                network={{
                ssid="{ssid}"
                psk="{password}"
                key_mgmt=WPA-PSK
                }}
                """
            try:
                with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
                    f.write(wpa_supplicant_conf)
                subprocess.call(["wpa_cli", "-i", "wlan0", "reconfigure"])
                subprocess.call(["dhclient", "wlan0"])
            except Exception as e:
                print("An error occurred while trying to connect to the Wi-Fi network.")
                print(e)

                ip_address = subprocess.check_output(["hostname", "-I"]).decode().strip()
            if not ip_address:
                print(
                    "Could not retrieve IP address. Please check if the Wi-Fi credentials are correct and the network is in range.")

            print("Connected to Wi-Fi network: ", ssid)
            print("IP address: ", ip_address)

        else:
            return HttpResponse("Missing ssid or password")
    return render(request, 'login.html')
