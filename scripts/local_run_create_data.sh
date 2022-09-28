#! /bin/bash

export PYTHONPATH=$PYTHONPATH:../


python3 tests/create_data/create_users.py
python3 tests/create_data/create_devices.py
