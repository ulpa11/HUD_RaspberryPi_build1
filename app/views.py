from django.shortcuts import render, redirect
import subprocess
from hardware  import call_function
#import json responce
from django.http import JsonResponse
from django.http import HttpResponse



def button_callback(channel):
    print("Button was pushed!")
    state = True

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
            return redirect('reading_data')

        else:
            return HttpResponse("Missing ssid or password")
    return render(request, 'login.html')

def reading_data(request):
    if request.method=="POST":
        return redirect('treatment_running')
    return render(request, 'reading_data.html')


def treatment_running(request):
    #run call function
    call_function()
    return render(request, 'treatment_running.html')

# def wifi_names(request):
#     try:
#         result = subprocess.run(["iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
#         output = result.stdout.decode("utf-8")
#         ssid_list = []
#         for line in output.split("\n"):
#             if "ESSID:" in line:
#                 ssid = line.split("ESSID:")[1].strip('"')
#                 ssid_list.append(ssid)
#         return JsonResponse(ssid_list, safe=False)
#     except Exception as e:
#         print("An error occurred while trying to retrieve the Wi-Fi network names.")
#         print(e)
#         return HttpResponse("An error occurred while trying to retrieve the Wi-Fi network names.")
                

def wifi_names(request):
    try:
        result = subprocess.run(["iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        ssid_list = []
        for line in output.split("\n"):
            if "ESSID:" in line:
                ssid = line.split("ESSID:")[1].strip('"')
                ssid_list.append(ssid)
        return render(request, 'wifi_names.html', {'ssid_list': ssid_list})
    except Exception as e:
        print("An error occurred while trying to retrieve the Wi-Fi network names.")
        print(e)
        return HttpResponse("An error occurred while trying to retrieve the Wi-Fi network names.")
