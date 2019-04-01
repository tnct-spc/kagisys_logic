# -*- coding: utf-8 -*-

"""This program is door sensor (magnetic reed switch) contral model."""

import signal
import RPi.GPIO as GPIO
import time


class Door():
    """This class contral read switch."""

    def __init__(self):
        """Set gpio and exit handler."""
        # set exit handler
        signal.signal(signal.SIGINT, self.exit_handler)

        # set gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20,GPIO.OUT)
        GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(20,1)

    def exit_handler(self):
        """Exit handler."""
        print("Exit motor")
        GPIO.cleanup()

    def isClose(self):
        """check door state."""
        # contral servo
	return GPIO.input(21)

