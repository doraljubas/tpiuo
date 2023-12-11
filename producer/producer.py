import json
from time import sleep

import azure.eventhub as eh
import requests
from azure.eventhub import EventData

CONN_STR = "Endpoint=sb://fv-lab1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YQDCiSnN9B6XM+qWTrIWPlUvVW4/tySt1+AEhKUqyWk="
EVENTHUB_NAME = "reddit-hub"


def fetch_top_dataengineering_posts(after):
    url = "https://www.reddit.com/r/dataengineering/top.json"
    params = {
        "limit": 10,
        "t": "all",
        "after": after
    }
    return requests.get(url, params=params, headers={"User-agent": "fer-lab1"}).json()


def send_posts_to_event_hub(posts):
    producer = eh.EventHubProducerClient.from_connection_string(conn_str=CONN_STR, eventhub_name=EVENTHUB_NAME)
    event_data_batch = producer.create_batch()
    for post in posts:
        body = json.dumps(post.get("data")).encode('utf-8')
        event_data_batch.add(event_data=EventData(body=body))
    producer.send_batch(event_data_batch)


after = None
while True:
    response = fetch_top_dataengineering_posts(after)
    posts = response.get("data", {}).get("children", [])
    after = response.get("data", {}).get("after", None)
    if after is None:
        break
    send_posts_to_event_hub(posts)
    # sleep(10)
