#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 
import time
from db_access import DatabaseAccess

BUZZER_PIN = 17
BUZZER_FREQUENCY = 900
BUZZER_DUTY_CYCLE = 50
BUZZER_DURATION = 0.2

CARD_READER_DELAY = 1.5

def buzzer_beep():
        pwm.start(BUZZER_DUTY_CYCLE)
        time.sleep(BUZZER_DURATION)
        pwm.stop()

if __name__ == "__main__":
   
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, BUZZER_FREQUENCY)
    reader = SimpleMFRC522()

    try:
        while True:
            id = reader.read_id()
            buzzer_beep()
            if DatabaseAccess.IsKartaValid(id):
                added = DatabaseAccess.AddPruchod(id)
            # else:
            #     print("card is not valid")
            time.sleep(CARD_READER_DELAY)

    except KeyboardInterrupt:
        print("Reader Stopped!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up")

