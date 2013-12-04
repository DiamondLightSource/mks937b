#!/bin/env dls-python2.6

import re
from pkg_resources import require
require("dls_serial_sim")

from dls_serial_sim import serial_device, CreateSimulation


class Channel(object):
    def __init__(self, gauge_type):
        self.type = gauge_type
        self.pressure = 0.01
        self.controlSetPoint = 1.0E-6
        self.relaySetPoint = 1.0E-6
        self.protectionSetPoint = 1.0E-6
        self.cathodeEnable = "OFF"
        self.power = "OFF"
        self.cathodeControl = "OFF"
        self.cathodeHysteresis = 0.0
        self.relayHysteresis = 0.0
        self.relayMode = "SET"
        self.relayDirection = "ABOVE"
        self.fastRelaySetPoint = 1.0E-7

    def getPressure(self):
        result = '%.1E' % self.pressure
        if self.type == 'img':
            if not self.cathodeEnable:
                result = 'HV_OFF'
            elif self.pressure > 0.01:
                result = 'HI'
        elif self.type == 'pirani':
            if self.pressure < 0.001:
                result = 'LO'
        else:
            result = 'NOGAUGE!'
        return result

class Mks937bController(serial_device):

    Terminator = ";FF"

    def __init__(self, address="001", tcpPort=None, ui=None, name='none'):
        self.address = address
        self.chan_ack = "@%sACK" % self.address
        self.name = name
        serial_device.__init__(self, ui=ui)
        self.unit = "mbar"
        self.channels = [Channel("img"),
                         Channel("img"),
                         Channel(""),
                         Channel("pirani"),
                         Channel("pirani")]
        self.controller_funcs = {"U": lambda: "@%sACK%s" % (address, self.unit),
                                 "FV6": lambda: "@%sACK6.0" % address,
                                 "FV5": lambda: "@%sACK5.0" % address,
                                 "MT": lambda: "@%sACKHC,CC,T1" % address}
        if tcpPort is not None:
            self.start_ip(tcpPort)

    def request(self, command_type, channel):
        if command_type == "PR":
            return "%s%s" % (self.chan_ack, channel.getPressure())
        elif command_type == "CP":
            return "%s%s" % (self.chan_ack, channel.power)
        elif command_type == "SP":
            return "%s%.3E" % (self.chan_ack, channel.relaySetPoint)
        elif command_type == "CSP":
            return "%s%.3E" % (self.chan_ack, channel.controlSetPoint)
        elif command_type == "CTL":
            return "%s%s" % (self.chan_ack, channel.cathodeEnable)
        elif command_type == "CSE":
            return "%s%s" % (self.chan_ack, channel.cathodeControl)
        elif command_type == "PRO":
            return "%s%.3E" % (self.chan_ack, channel.protectionSetPoint)
        elif command_type == "SH":
            return "%s%.1E" % (self.chan_ack, channel.relayHysteresis)
        elif command_type == "EN":
            return "%s%s" % (self.chan_ack, channel.relayMode)
        elif command_type == "SD":
            return "%s%s" % (self.chan_ack, channel.relayDirection)
        elif command_type == "CHP":
            return "%s%.1E" % (self.chan_ack, channel.cathodeHysteresis)
        elif command_type == "FRC":
            return "%s%.1E" % (self.chan_ack, channel.fastRelaySetPoint)

    def set_value(self, command_type, channel, value):
        if command_type == "PR":
            try:
                channel.pressure = float(value)
            except ValueError:
                pass
            return "%s%s" % (self.chan_ack, channel.getPressure())
        elif command_type == "CP":
            if value in ("ON", "OFF"):
                channel.power = value
            return "%s%s" % (self.chan_ack, channel.power)
        elif command_type == "SP":
            try:
                channel.relaySetPoint = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.relaySetPoint)
        elif command_type == "CSP":
            try:
                channel.controlSetPoint = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.controlSetPoint)
        elif command_type == "CTL":
            if value in ("OFF", "SAFE", "AUTO"):
                channel.cathodeEnable = value
            return "%s%s" % (self.chan_ack, channel.cathodeEnable)
        elif command_type == "CSE":
            if value in ("A1", "B1", "A2", "B2", "C1", "C2", "OFF"):
                channel.cathodeControl = value
            return "%s%s" % (self.chan_ack, channel.cathodeControl)
        elif command_type == "PRO":
            try:
                channel.protectionSetPoint = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.protectionSetPoint)
        elif command_type == "SH":
            try:
                channel.relayHysteresis = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.relayHysteresis)
        elif command_type == "EN":
            if value in ("SET", "CLEAR", "ENABLE"):
                channel.relayMode = value
            return "%s%s" % (self.chan_ack, channel.relayMode)
        elif command_type == "SD":
            if value in ("ABOVE", "BELOW"):
                channel.relayDirection = value
            return "%s%s" % (self.chan_ack, channel.relayDirection)
        elif command_type == "CHP":
            try:
                channel.relayHysteresis = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.relayHysteresis)
        elif command_type == "FRC":
            try:
                channel.fastRelaySetPoint = float(value)
            except ValueError:
                pass
            return "%s%.1E" % (self.chan_ack, channel.fastRelaySetPoint)


    def reply(self, command):
        command = command.lstrip() # telnet has a leading /n so remove
        print command
        command_type = re.search(
            "PRO|CP|SP|SH|EN|SD|PR|FRC|CSP|CHP|CTL|CSE|DG|U|FV6|FV5|MT",
            command)
        if command_type:
            command_type = command_type.group(0)
        else:
            return
        if command[:4] != "@%s" % self.address:
            print "Bad command", command
            return "Bad command"
        if command_type in self.controller_funcs:
            return self.controller_funcs[command_type]()
        channel = self.channels[int(command[4+len(command_type)]) - 1]
        if command[5+len(command_type)] == "?":
            return self.request(command_type, channel)
        elif command[5+len(command_type)] == "!":
            value = command[6+len(command_type):]
            return self.set_value(command_type, channel, value)
        #return command

if __name__ == "__main__":
    # run our simulation on the command line. Run this file with -h for help
    CreateSimulation(Mks937bController)
    raw_input()
