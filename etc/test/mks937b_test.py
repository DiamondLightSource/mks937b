#!/bin/env dls-python2.6

# Test suite to use with pyUnit

import sys
from pkg_resources import require
require('dls_autotestframework')

from dls_autotestframework import *

################################################
# Test suite for the MKS 937A Gauge Controller

   
class mks937aTestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        Target("example_sim", self, entities = [
            IocEntity('ioc', directory="iocs/example_sim", bootCmd="bin/linux-x86/stexample.sh"),
            EpicsDbEntity('db', fileName="iocs/example_sim/db/example_expanded.db"),
            BuildEntity('build', directory='.'),            
            SimulationEntity('controller', runCmd="./data/Mks937aCrate.py -i 7001 -r 9001", rpcPort=9001),
#            EnvironmentEntity('EPICS_CA_REPEATER_PORT','6065'),
#            EnvironmentEntity('EPICS_CA_SERVER_PORT','6064'),
#            GuiEntity('gui', runCmd='iocs/example_sim/bin/linux-x86/stexample-gui')
        ])

        # The tests
        CaseGetFrequency(self)
        
################################################
# Intermediate test case class that provides some utility functions
# for this suite

class mks937aCase(TestCase):
    base_pvname = "TEST-VA-GCTLR-01"
    pv_getfreq  = base_pvname+":F"
        
        
################################################
# Test cases
    
class CaseGetFrequency(mks937aCase):
    def runTest(self):
        print "mks937aTestSuite - CaseGetFrequency()"
        '''The GetFrequency test'''
        if self.simulationDevicePresent("mks937a"):
            self.diagnostic("frequency read = %s" % (self.getPv(self.pv_getfreq)),1)
            f = self.getPv(self.pv_getfreq)
            self.verifyInRange(f, 50, 60)

            
################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    mks937aTestSuite()
    # run this as ./etc/test/mks937a_test.py -i -e -g

    
