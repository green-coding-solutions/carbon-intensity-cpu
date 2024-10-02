#!/bin/bash
set -euo pipefail

sudo cp io.green-coding.carbon-intensity-cpu.plist /Library/LaunchDaemons/
sudo sed -i '' s#__PWD__#$(pwd)#g /Library/LaunchDaemons/io.green-coding.carbon-intensity-cpu.plist

sudo launchctl load /Library/LaunchDaemons/io.green-coding.carbon-intensity-cpu.plist