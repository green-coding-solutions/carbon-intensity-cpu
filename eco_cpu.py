import os
import sys
import requests
import argparse
import configparser
import glob

def read_config(file_path, args):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {
        'lat': config.getfloat('Settings', 'lat', fallback=args.lat),
        'lng': config.getfloat('Settings', 'lng', fallback=args.lng),
        'wg': config.getint('Settings', 'wg', fallback=args.wg),
        'token': config.get('Settings', 'token', fallback=args.token),
        'powersave_state': config.get('Settings', 'token', fallback=args.powersave_state),
        'performance_state': config.get('Settings', 'token', fallback=args.performance_state),
    }

def get_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    location = data["loc"].split(",")
    latitude = location[0]
    longitude = location[1]
    return latitude, longitude


def get_carbon_intensity(latitude, longitude, token):

    headers = {}
    if token:
        headers['auth-token'] = token

    params = {'lat': latitude, 'lon': longitude }

    response = requests.get('https://api.electricitymap.org/v3/carbon-intensity/latest', params=params, headers=headers, timeout=10)
    if response.status_code == 200:
        resp_data = response.json()
        return resp_data.get('carbonIntensity')

    return None

def get_cpus_supporting_governors(powersave, performance ):
    required_governors = {powersave, performance}

    cpu_governors_paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_available_governors")

    supported_cpus = []

    for path in cpu_governors_paths:
        try:
            with open(path, 'r') as file:
                available_governors = set(file.read().strip().split())
                if required_governors.issubset(available_governors):
                    cpu_num = path.split('/')[5][3:]
                    supported_cpus.append(cpu_num)
        except IOError as e:
            print(f"Error reading {path}: {e}")

    return supported_cpus

def set_cpu_state(state, supported_cpus):
    governor_paths = [f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor" for cpu in supported_cpus]

    for path in governor_paths:
        try:
            with open(path, 'w') as file:
                file.write(state)
        except IOError as e:
            print(f"Error setting {state} governor for {path}: {e}")
            raise e

if __name__ == '__main__':

    if not os.geteuid() == 0:
        print("This script must be run as root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='A little script that sets your computers performance according to the energy grids carbon intensity.')

    parser.add_argument('-c', type=str, default='/etc/eco-cpu.conf', help='Path to the config file (default: /etc/eco-cpu.conf)')
    parser.add_argument('--powersave-state', type=str, default='powersave', help='The name of the power save state in your CPU (default: powersave)')
    parser.add_argument('--performance-state', type=str, default='performance', help='The name of the performance state in your CPU default: performance)')
    parser.add_argument('--lat', type=float, required=False, help='Latitude')
    parser.add_argument('--lng', type=float, required=False, help='Longitude')
    parser.add_argument('-wg', type=int, default=100, help='Integer when power should be considered green (default: 100)')
    parser.add_argument('--token', type=str, required=False, help='Electricitymaps access token. Get your token under https://api-portal.electricitymaps.com/')
    args = parser.parse_args()

    if os.path.exists(args.c):
        config_values = read_config(args.c)
    else:
        config_values = args

    if config_values.lat is None or config_values.lng is None:
        config_values.lat, config_values.lng = get_location()

    if not config_values.token:
        print('Token is not set. We will try without but this might not work! Please set one either as parameter or in the config file.')

    cpus = get_cpus_supporting_governors(config_values.powersave_state, config_values.performance_state)

    ci = get_carbon_intensity(config_values.lat, config_values.lng, config_values.token)

    if ci <= config_values.wg:
        set_cpu_state(config_values.performance_state, cpus)
        print(f"Carbon intensity is {ci}, set CPUs into {config_values.performance_state}")
    else:
        set_cpu_state(config_values.powersave_state, cpus)
        print(f"Carbon intensity is {ci}, set CPUs into {config_values.powersave_state}")

