TOP=../..

include $(TOP)/configure/CONFIG

USR_CFLAGS += -DEPICS_R3_14

# The following switch is required if compiling C++
# gensub modules, as the genSubRecord structure declares
# a member 'unsigned long	not;'
# However, 'not' has been made a non-ansi reserved word
# but can be switch off as such by this compiler switch :)
USR_CXXFLAGS_DEFAULT += -fno-operator-names
USR_CXXFLAGS_DEFAULT += -pedantic


#==================================================
# build a mks937b library
#

LIBRARY_IOC += mks937b

# install support.dbd into <top>/dbd
DBD += mks937b.dbd

mks937b_DBD += base.dbd
#mks937b_DBD += genSubRecord.dbd
mks937b_DBD += mks937bRegister.dbd

# specify all source files to be compiled and added to the library
mks937b_SRCS += mks937bMean.c

mks937b_LIBS += $(EPICS_BASE_IOC_LIBS)

DATA += mks937b_sim.py

include $(TOP)/configure/RULES
