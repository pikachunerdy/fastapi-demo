#! /bin/bash
cd ..

cd ./company-device-service
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
deactivate
cd ..

cd ./company-account-service
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
deactivate
cd ..
