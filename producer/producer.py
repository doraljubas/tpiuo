import json

import azure.eventhub as eh
import requests
from azure.eventhub import EventData

CONN_STR = "Endpoint=sb://fv-lab1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YQDCiSnN9B6XM+qWTrIWPlUvVW4/tySt1+AEhKUqyWk="
EVENTHUB_NAME = "reddit-hub"


def fetch_top_dataengineering_posts():
    url = "https://www.reddit.com/r/dataengineering/top.json"
    params = {
        "limit": "all",
        "t": 10
    }
    response = requests.get(url, params=params, headers={"User-agent": "fer-lab1"})
    # print(response.json())
    return response.json().get("data").get("children")


def send_posts_to_event_hub(posts):
    producer = eh.EventHubProducerClient.from_connection_string(conn_str=CONN_STR, eventhub_name=EVENTHUB_NAME)
    event_data_batch = producer.create_batch()
    for post in posts:
        # print(post.get("data"))
        body = json.dumps(post.get("data")).encode('utf-8')
        event_data_batch.add(event_data=EventData(body=body))
    producer.send_batch(event_data_batch)


print("Start sending data to event hub!!!!")
top_posts = fetch_top_dataengineering_posts()
send_posts_to_event_hub(top_posts)
print("End sending data to event hub")
