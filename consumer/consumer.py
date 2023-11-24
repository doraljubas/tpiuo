from azure.eventhub import EventHubConsumerClient

CONN_STR = "Endpoint=sb://fv-lab1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YQDCiSnN9B6XM+qWTrIWPlUvVW4/tySt1+AEhKUqyWk="
EVENTHUB_NAME = "reddit-hub"
CONSUMER_GROUP = "$Default"

client = EventHubConsumerClient.from_connection_string(CONN_STR, CONSUMER_GROUP, eventhub_name=EVENTHUB_NAME)


def on_event(partition_context, event):
    print(event.body_as_str(encoding='UTF-8'))
    partition_context.update_checkpoint(event)


with client:
    client.receive(on_event=on_event)
print("DONE!")
