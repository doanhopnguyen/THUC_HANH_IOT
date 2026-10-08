import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/sensor01/data"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        temperature = round(random.uniform(25, 40), 1)
        humidity = round(random.uniform(30, 80), 1)

        data = {
            "device_id": "sensor01",
            "temperature": temperature,
            "humidity": humidity
        }

        payload = json.dumps(data)

        client.publish(TOPIC, payload)

        print("Da gui:")
        print(payload)

        time.sleep(3)

except KeyboardInterrupt:
    print("\nDung sensor")
    client.loop_stop()
    client.disconnect()