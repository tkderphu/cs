# Note about MQTT

MQTT stands for Message Queuing Telemetry Transport


It's a lightweight publish/subscribe messaging protocol often used for comminucation between devices in IoT systems

- Lightweight & efficient
    - Designed for devices with limited processing power, memory, or network bandwith

- Publish/subscribe model
    - Instead of sending messages directly from one device to another, devices publish messages to a "topic" on a broker. Other devices subscribe to those topics to receives message
- Broker-based
    - MQTT requires a central broker(like Mosquitto) that handles distributing messages between publishers and subscribers
- Low bandwith & reliable over unstable networks
    - That's why it's common in IoT, smart home, and industrial monitoring


# Install server

In this section i will use Mosquitto

```
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

- MQTT broker running on localhost:1833

# Publish and subscribe

Mosquitto comes with command-line tools:

- Subscribe to a topic:

```
mosquitto_sub -h localhost -t "test/topic"
```

- Publish a message

```
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```

- The subscriber will immediately receive Hello MQTT.