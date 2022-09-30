FROM python:3.10-slim

COPY ./libs /libs
COPY ./schemas /schemas
COPY ./device_coap_service/configs ./configs
COPY ./device_coap_service/scripts ./scripts
COPY ./device_coap_service/configs ./configs
COPY ./device_coap_service/main.py ./main.py
COPY ./device_coap_service/requirements.txt ./requirements.txt
COPY ./device_coap_service/entrypoint.sh ./entrypoint.sh

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]
