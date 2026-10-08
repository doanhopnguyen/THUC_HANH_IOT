import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/message"

HO_TEN = "Nguyen Doan Hop"
MA_SV = "B23DCC350"

message = f"Xin chao tu client Python MQTT - {MA_SV} - {HO_TEN}"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT, 60)

client.loop_start()

result = client.publish(TOPIC, message)
result.wait_for_publish()

print("Da gui message:")
print(message)

client.loop_stop()
client.disconnect()