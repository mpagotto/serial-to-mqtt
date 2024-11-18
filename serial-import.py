import serial
import paho.mqtt.client as mqtt
import time

# Serial port configuration
SERIAL_PORT = '/dev/tty.usbserial-0001'
BAUD_RATE = 115200  # Update this as needed

# MQTT broker configuration
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883  # Update this as needed (default port)
MQTT_TOPIC = 'topic'

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to serial port: {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    exit(1)

# Initialize MQTT client
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")


client.on_connect = on_connect

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    while True:
        # Read line from serial console
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            #print(f"Read from serial: {line}")

            # Publish to MQTT
            client.publish(MQTT_TOPIC, line)
            #print(f"Published to MQTT: {line}")

        # Add a small delay to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Script interrupted by user")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Cleanup
    ser.close()
    client.loop_stop()
    client.disconnect()
    print("Serial connection closed and MQTT disconnected")