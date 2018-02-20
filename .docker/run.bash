#!/bin/bash

WS=${HOME}/keymint_ws
mkdir -p ${WS}

IMAGE="keymint/keymint_tools"

source keymint-docker.bash $@
