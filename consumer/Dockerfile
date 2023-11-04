FROM python:3.8-slim
LABEL authors="doralj"

WORKDIR /consumer-service

RUN pip install azure-eventhub

COPY consumer.py .

CMD [ "python", "consumer.py" ]