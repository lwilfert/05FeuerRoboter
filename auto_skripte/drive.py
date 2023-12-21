import time
from time import sleep
import requests

ip = "192.168.171.91"

def send_control_request():
    url = f"{ip}:5000/go"
    body = {"value": 0.2}
    response = requests.post(url, json=body)
    print(response.text)
    sleep(2)
    stop_control_request()

def stop_control_request():
    url = f"{ip}:5000/stop"
    response = requests.post(url)
    print(response.text)

def main():
    send_control_request()
    time.sleep(5)
    stop_control_request()

if __name__ == "__main__":
    main()

