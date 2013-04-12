#!/bin/env dls-python2.6

import re
from pkg_resources import require
require("dls_serial_sim")

from dls_serial_sim import serial_device, CreateSimulation


class Channel(object):
    def __init__(self, gauge_type):
        self.type = gauge_type
        self.pressure = 0.0001
        self.controlSetPoint = 0.0
        self.relaySetPoint = 0.0
        self.protectionSetPoint = 0.0
        self.coldCathodeEnable = True

    def getPressure(self):
        result = '%.1E' % self.pressure
        if self.type == 'img':
            if not self.coldCathodeEnable:
                result = 'HV_OFF'
            elif self.pressure > 0.01:
                result = 'HI'
        elif self.type == 'pirani':
            if self.pressure < 0.001:
                result = 'LO'
        else:
            result = 'NOGAUGE!'
        return result

class Controller(serial_device):

    Terminator = ";FF"

    def __init__(self, address):
        self.address = address
        serial_device.__init__(self, ui=None)
        self.channels = [Channel("img"),
                         Channel("img"),
                         Channel(""),
                         Channel("pirani"),
                         Channel("pirani")]


    def reply(self, command):
        if not command or command[0:4] != "@%s" % self.address:
            return "Bad command"
        command_type = re.search(
            "PR|CP|SP|SH|EN|SD|PRO|FRC|CSP|CHP|CTL|CSE|DG|U|FV6|FV5|MT",
            command).group(0)

        return command

if __name__ == "__main__":
    # run our simulation on the command line. Run this file with -h for help
    CreateSimulation(Controller, "001")
    raw_input()
