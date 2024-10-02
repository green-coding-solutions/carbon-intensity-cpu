#!/bin/bash
set -euo pipefail

sudo launchctl unload /Library/LaunchDaemons/io.green-coding.carbon-intensity-cpu.plist
sudo rm /Library/LaunchDaemons/io.green-coding.carbon-intensity-cpu.plist