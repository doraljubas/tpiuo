import json
import random
from datetime import datetime
from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient


CONN_STR = "Endpoint=sb://fv-lab1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YQDCiSnN9B6XM+qWTrIWPlUvVW4/tySt1+AEhKUqyWk="
EVENTHUB_NAME = "reddit-hub"
CONSUMER_GROUP = "$Default"

STORAGE_ACCOUNT_URL = "https://safervjestina.dfs.core.windows.net"
STORAGE_ACCOUNT_KEY = "AfQ+3+VclUt8+53NtKlDh+Aitkesd6jpIBquzVNDzkcONo7CpDQKRc0N2ACz7klsB3EKRM30qYJy+AStuMHIqg=="
CONTAINER_NAME = "lab2"

event_hub_client = EventHubConsumerClient.from_connection_string(CONN_STR, CONSUMER_GROUP, eventhub_name=EVENTHUB_NAME)


def get_service_client_account_key() -> DataLakeServiceClient:
    service_client = DataLakeServiceClient(STORAGE_ACCOUNT_URL, credential=STORAGE_ACCOUNT_KEY)
    return service_client


def on_event(partition_context, event):
    message_body = json.loads(event.body_as_str(encoding='UTF-8'))

    created_timestamp = message_body.get("created")
    created_datetime = datetime.fromtimestamp(created_timestamp)
    directory_path = created_datetime.strftime("%Y/%m/%d/%H/%M")

    adls_client = get_service_client_account_key()

    file_system_client = adls_client.get_file_system_client(CONTAINER_NAME)
    dir_client = file_system_client.get_directory_client(directory_path)
    dir_client.create_directory()

    author = message_body.get("author_fullname")
    file_name=author +"_"+ str(random.randint(100000, 999999)) + ".json"
    file_client = dir_client.create_file(file_name)
    file_contents = json.dumps(message_body)
    file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
    file_client.flush_data(len(file_contents))

    print(file_name)
    partition_context.update_checkpoint(event)


with event_hub_client:
    event_hub_client.receive(on_event=on_event)

