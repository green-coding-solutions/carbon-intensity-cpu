#!/bin/bash
set -euo pipefail

THIS_SCRIPT_DIR=$(realpath $(dirname "$0"))
ECO_CPU_HOME="/usr/local/bin/eco-cpu"
CONF_FILE="/etc/eco-cpu.conf"

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

mkdir -p $ECO_CPU_HOME

cd $THIS_SCRIPT_DIR

cp start-eco-cpu.sh $ECO_CPU_HOME
chmod a+x "$ECO_CPU_HOME/start-eco-cpu.sh"

cp eco_cpu.py $ECO_CPU_HOME
chmod a+x "$ECO_CPU_HOME/eco_cpu.py"

cp eco_cpu.service /etc/systemd/system/eco_cpu.service
chmod 644 /etc/systemd/system/eco_cpu.service

cp eco_cpu.timer /etc/systemd/system/eco_cpu.timer
chmod 644 /etc/systemd/system/eco_cpu.timer


if [ ! -f "$CONF_FILE" ]; then
    echo "Enter your Electricity Maps token so we can get the grid intensity."
    echo "You can get one under https://api-portal.electricitymaps.com/"
    echo "Getting the grid intensity might also work without a token but this is not guaranteed."
    read -p "What is your token (leave blank if none): " token

    if [ ! -z "$token" ]; then
        echo "[Settings]" >> "$CONF_FILE"
        echo "token=$token" >> "$CONF_FILE"
        echo "Your token has been saved."
    else
        echo "No token was provided. Continuing without setting a token."
    fi
else
    echo "Configuration file $CONF_FILE already exists. You will need to update it manually"
fi

cd $ECO_CPU_HOME

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r $THIS_SCRIPT_DIR/requirements.txt

if systemctl is-active --quiet eco_cpu.timer; then
    systemctl restart eco_cpu.timer
    echo "eco_cpu.timer reloaded"
else
    systemctl start eco_cpu.timer
    systemctl enable eco_cpu.timer
fi

echo "!!! Install complete !!!"