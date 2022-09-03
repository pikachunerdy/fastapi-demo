#! /bin/bash
cd ./company_account_service/
sudo ./scripts/local_run &
cd ../
cd ./company_device_service/
sudo ./scripts/local_run &
cd ../
cd ./device_service
sudo ./scripts/local_run
cd ../
# sleep 30
# cd ./device_coap_service
# sudo ./scripts/local_run
sudo pkill python3
sudo pkill uvicorn
