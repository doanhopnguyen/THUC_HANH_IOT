import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
PORT = 1883
DEVICES = ["light01", "fan01", "pump01"]

status = {}
for device_id in DEVICES:
    status[device_id] = "OFF"


def publish_status(client, device_id):
    topic = f"iot/lab/{device_id}/status"

    data = {
        "device_id": device_id,
        "status": status[device_id]
    }

    payload = json.dumps(data)

    client.publish(topic, payload)

    print("Da gui trang thai:")
    print(payload)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Ket noi MQTT broker thanh cong")

        for device_id in DEVICES:
            topic = f"iot/lab/{device_id}/cmd"
            client.subscribe(topic)
            print("Dang lang nghe topic:", topic)
            publish_status(client, device_id)
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, msg):
    try:
        device_id = msg.topic.split("/")[2]
        command = msg.payload.decode("utf-8").strip().upper()

        print("\n------------------------")
        print("Thiet bi:", device_id)
        print("Nhan duoc lenh:", command)

        if command not in ("ON", "OFF"):
            print("Lenh khong hop le, bo qua")
            return

        status[device_id] = command

        if command == "ON":
            print(device_id, "da BAT")
        else:
            print(device_id, "da TAT")

        publish_status(client, device_id)

    except Exception as e:
        print("Loi xu ly lenh:", e)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDung thiet bi")
    client.disconnect()
