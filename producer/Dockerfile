FROM python:3.8-slim
LABEL authors="doralj"

WORKDIR /producer-service

RUN pip install azure-eventhub
RUN pip install requests

COPY producer.py .

CMD [ "python", "producer.py" ]