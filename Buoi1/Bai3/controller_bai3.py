import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
DEVICES = ["light01", "fan01", "pump01"]


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        for device_id in DEVICES:
            client.subscribe(f"iot/lab/{device_id}/status")
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")

    print("\nTrang thai nhan duoc:")
    print(payload)
    print("Nhap lenh: ", end="", flush=True)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

print("Thiet bi:", ", ".join(DEVICES))
print("Cu phap: ON | OFF | <thiet bi> ON | <thiet bi> OFF | EXIT")

try:
    while True:
        parts = input("Nhap lenh: ").strip().split()

        if len(parts) == 0:
            continue

        if len(parts) == 1:
            device_id = DEVICES[0]
            command = parts[0].upper()
        elif len(parts) == 2:
            device_id = parts[0].lower()
            command = parts[1].upper()
        else:
            print("Loi: sai cu phap. Vi du: ON, OFF, fan01 ON, EXIT")
            continue

        if len(parts) == 1 and command == "EXIT":
            break

        if device_id not in DEVICES:
            print("Loi: khong co thiet bi", device_id)
            continue

        if command not in ("ON", "OFF"):
            print("Loi: lenh khong hop le. Chi chap nhan ON, OFF hoac EXIT")
            continue

        topic = f"iot/lab/{device_id}/cmd"

        result = client.publish(topic, command)
        result.wait_for_publish()

        print("Da gui lenh", command, "toi", device_id)

except KeyboardInterrupt:
    pass

print("\nDung controller")
client.loop_stop()
client.disconnect()
