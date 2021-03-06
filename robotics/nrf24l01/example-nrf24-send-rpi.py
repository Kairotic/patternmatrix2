#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev


pipes = [[0x01, 0x01, 0x01, 0x1, 0x01], [0xa7, 0xa7, 0xa7, 0xa7, 0xa7]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(100)
radio.write_register(NRF24.FEATURE, 0)

#radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(False)
#radio.enableDynamicPayloads()
#radio.enableAckPayload()


radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()


c=1
while True:
#    buf = ['M', 0, 0, 0, 0, 0, 0, 0, 0,\
#           0, 0, 0, 0, 0, 0, 0, 0, 0,\
#           0, 0, 0, 0, 0, 0, 0, 0, 0,\
#           0, 0, 0, 0, 0, 0, 0, 0, 0]
    buf = ['H', 'E', 'L', 'O', c]

    c = (c + 1) & 255
    # send a packet to receiver
    radio.write(buf)
    #print ("Sent:"),
    #print (buf)
    #radio.printDetails()
    # did it return with a payload?
    if radio.isAckPayloadAvailable():
        pl_buffer=[]
        radio.read(pl_buffer, radio.getDynamicPayloadSize())
        print ("Received back:"),
        print (pl_buffer)
    #else:
    #    print ("Received: Ack only, no payload")
    time.sleep(1)
