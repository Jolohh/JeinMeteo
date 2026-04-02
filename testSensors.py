
import paho.mqtt.client as mqtt

from sense_hat import SenseHat

sense = SenseHat()

temperature = sense.get_temperature()

pressure = sense.get_pressure()

sense.show_message(f"P: {pressure:.2f}")

sense.show_message(f"T: {temperature:.2f}")
