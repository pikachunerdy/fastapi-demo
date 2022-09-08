FROM python:3.10-slim

COPY ./company-account-service/app /app
COPY ./company-account-service/entrypoint.sh /entrypoint.sh
COPY ./company-account-service/gunicorn.config.py /gunicorn.config.py
COPY ./company-account-service/requirements.txt /requirements.txt
COPY ./company-account-service/scripts /scripts
COPY ./company-account-service/ca-certificate.crt /ca-certificate.crt

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