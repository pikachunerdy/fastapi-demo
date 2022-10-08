#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../
source ./setenv
python3 tests/create_data/create_users.py
python3 tests/create_data/create_devices.py
python3 tests/create_data/create_coap_message.py
