"""Module providingFunction digesting JSON."""
import json
import random
import datetime
import time
import requests


def generate_random_timestamps(interval_minutes, num_timestamps):
    """Generate random timestamps for events during business hours 8-5 over
    the last 7 days during"""
    timestamp_list = []
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    while start_date <= end_date:
        if start_date.time() >= datetime.time(8, 0) \
         and start_date.time() <= datetime.time(17, 0):
            for _ in range(num_timestamps):
                random_second = random.uniform(0, 59.999)
                timestamp = start_date.timestamp() + random_second
                timestamp = f"{timestamp:0.3f}"
                timestamp_list.append(timestamp)

        start_date += datetime.timedelta(minutes=interval_minutes)
    print("Generated random timestamps for past logs")
    return timestamp_list


def generate_single_timestamp():
    new_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=15)
    new_timestamp = f"{new_timestamp.timestamp():0.3f}"
    return new_timestamp


# Constants & Variables
#API_ENDPOINT_JSON = "https://cloud.community.humio.com/api/v1/ingest/json"
#API_ENDPOINT_HEC = "https://cloud.community.humio.com/api/v1/ingest/hec/raw"
API_ENDPOINT_JSON = "https://cloud.us.humio.com/api/v1/ingest/json"
API_ENDPOINT_HEC = "https://cloud.us.humio.com/api/v1/ingest/hec/raw"
API_KEY = "Your-Ingest-API-Key"
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': 'Bearer ' + API_KEY,
}
INTERVAL_IN_MINUTES = 15
TIMESTAMPS_PER_INTERVAL = 15
generated_random_events = []
userList = ["Amy", "Phillip", "Hermes", "Zapp", "Kif", "Leela", "Dwight",
            "Bender", "Farnsworth", "Zoidberg"]

# Create timestamps
random_timestamps = generate_random_timestamps(INTERVAL_IN_MINUTES,
                                               TIMESTAMPS_PER_INTERVAL)

# Open Sample Events List
data = open('events.json', encoding="utf-8")
eventsList = json.load(data)


for i in range(len(random_timestamps)):
    j = i % (len(eventsList["records"])-1)
    currentUser = userList[random.randint(0, len(userList)-1)]
    eventsList["records"][j]["time"] = random_timestamps[i]
    eventsList["records"][j]["device_user"] = currentUser
    if eventsList["records"][j]["os_platform"] == "Windows":
        eventsList["records"][j]["device_name"] = currentUser + '-Windows'
    else:
        eventsList["records"][j]["device_name"] = currentUser + '-Ubuntu'
    generated_random_events.append(eventsList["records"][j].copy())

with open("sample.json", "w", encoding="utf-8") as outfile:
    json.dump(generated_random_events, outfile, indent=0)
print("Created list of randomized logs")


"""
Creating the Post request to send bulk events via: 
curl https://cloud.community.humio.com/api/v1/ingest/json  -X POST
-H "Content-Type: application/json; charset=utf-8"
-H "Authorization: Bearer <ingest_token>
--data "@sample.json" 
"""


with open('sample.json', encoding="utf-8") as f:
    data = f.read().replace('\n', '').replace('\r', '').encode()

response = requests.post(API_ENDPOINT_JSON, headers=headers, data=data)
print(response)
print("Sent API POST request to LogScale for past logs")


# continuously generate logs to send to logscale by picking
# random log from generated_random_events with a new timestamp
while generated_random_events:
    time.sleep(random.randint(1, 10))
    single_event = (generated_random_events[random.randint(0, len(generated_random_events)-1)])
    single_event["time"] = generate_single_timestamp()
    event_to_send = json.dumps(single_event)
    response = requests.post(API_ENDPOINT_HEC, headers=headers, data=event_to_send)
    print("Log sent! Press Ctrl+C to cancel")
