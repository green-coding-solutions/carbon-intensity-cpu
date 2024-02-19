#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(realpath $(dirname "$0"))
ECO_CPU_HOME="/usr/local/bin/eco-cpu"
PYTHON_PATH='/usr/local/bin/eco-cpu/venv/bin/python3'

CMD="$PYTHON_PATH $ECO_CPU_HOME/eco_cpu.py"

eval $CMD