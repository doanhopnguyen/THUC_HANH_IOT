import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/sensor01/data"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Ket noi MQTT broker thanh cong")
        client.subscribe(TOPIC)
        print("Dang lang nghe topic:", TOPIC)
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))

        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]

        print("\n------------------------")
        print("Device:", device_id)
        print("Temperature:", temperature, "C")
        print("Humidity:", humidity, "%")

        if temperature > 35:
            print("CANH BAO: Nhiet do cao")

        if humidity < 40:
            print("CANH BAO: Do am thap")

    except Exception as e:
        print("Loi xu ly du lieu:", e)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDung monitor")
    client.disconnect()