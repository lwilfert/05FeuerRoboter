import requests


class ApiAdapter:
    def __init__(self, ip: str = "192.168.171.85", port: int = 5000):
        self.base_url = f"http://{ip}:{port}"

    def send_go_request(self, speed=0.12):
        url = f"{self.base_url}/go"
        body = {"value": speed}

        response = requests.post(url, json=body)
        print(response.text)
        return response

    def send_stop_request(self):
        url = f"{self.base_url}/stop"
        response = requests.post(url)

        print(response.text)
        return response

    # No difference between /right and /left, so always use right
    def send_right_request(self, value=70):
        url = f"{self.base_url}/right"
        body = {"value": value}

        response = requests.post(url, json=body)
        print(response.text)
        return response

    def send_left_request(self, value=110):
        url = f"{self.base_url}/right"
        body = {"value": value}

        response = requests.post(url, json=body)
        print(response.text)
        return response

    def send_center_request(self, value=90):
        url = f"{self.base_url}/right"
        body = {"value": value}

        response = requests.post(url, json=body)
        print(response.text)
        return response
