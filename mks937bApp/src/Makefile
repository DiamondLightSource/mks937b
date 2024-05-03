TOP=../..

include $(TOP)/configure/CONFIG

#==================================================
# build a mks937b library
#

LIBRARY_IOC += mks937b

# install support.dbd into <top>/dbd
DBD += mks937b.dbd

mks937b_DBD += base.dbd
mks937a_DBD += aSubRecord.dbd
mks937b_DBD += mks937bRegister.dbd

# specify all source files to be compiled and added to the library
mks937b_SRCS += mks937bMean.c

mks937b_LIBS += $(EPICS_BASE_IOC_LIBS)

DATA += mks937b_sim.py

include $(TOP)/configure/RULES
