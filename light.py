#!/usr/local/bin/python

import RPi.GPIO as GPIO
import redis
import time
import os
import datetime
import json

TOPIC = os.getenv('REDIS_TOPIC', 'test-topic')
REDIS_HOST = os.getenv('REDIS_PORT_6379_TCP_ADDR', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT_6379_TCP_PORT', 6379)
DT = float(os.getenv('DT', '1'))

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7

def rc_time (pin_to_circuit):
    count = 0

    #Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

if __name__ == "__main__":
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    #Catch when script is interrupted, cleanup correctly
    try:
        # Main loop
        while True:
            msg = {
                'timestamp': datetime.datetime.now().isoformat(),
                'key': 'light',
                'value': rc_time(pin_to_circuit)
            };
            print msg
            r.publish(TOPIC, json.dumps(msg))
            time.sleep(DT)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
