import subprocess
import urllib.request
import urllib.parse
import json
from urllib.error import HTTPError, URLError


def get_carbon_intensity(latitude, longitude, token=None):
    base_url = 'https://api.electricitymap.org/v3/carbon-intensity/latest'
    params = {}  # Add your parameters here if needed
    headers = {}  # Add your headers here

    # Encode parameters
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{encoded_params}"

    # Create request with headers
    req = urllib.request.Request(full_url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                data = response.read().decode('utf-8')
                resp_data = json.loads(data)
                return resp_data.get('carbonIntensity')
    except HTTPError as e:
        print(f"HTTP error: {e.code}")
    except URLError as e:
        print(f"URL error: {e.reason}")
    except TimeoutError:
        print("Request timed out")




def notify(message):
    subprocess.run(['launchctl', 'asuser', '501', 'osascript', '-e', f"display notification \"{message}\""], check=True)


def get_location():
    url = "https://ipinfo.io/json"

    with urllib.request.urlopen(url, timeout=10) as response:
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            location = data["loc"].split(",")
            latitude = location[0]
            longitude = location[1]
            return latitude, longitude
        raise RuntimeError(f"Response code was not 200: {response.getcode()}")



if __name__ == '__main__':
    try:

        latitude, longitude = get_location()
        ci = get_carbon_intensity(latitude, longitude)
        if ci > 200:
            notify(f"Setting to low power mode. The grid is dirrrrrrrty {ci}")
            subprocess.run(['sudo', 'pmset', '-a', 'lowpowermode', '1'], check=True)
        else:
            notify(f"Going back to normal mode. The grid is fine {ci}")
            subprocess.run(['sudo', 'pmset', '-a', 'lowpowermode', '0'], check=True)

    except Exception as e:
        notify(str(e))