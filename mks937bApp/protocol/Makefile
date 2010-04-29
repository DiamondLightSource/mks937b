TOP = ../..

ifdef EPICS_HOST_ARCH

include $(TOP)/configure/CONFIG
DATA += $(patsubst ../%, %, $(wildcard ../*.protocol))
include $(TOP)/configure/RULES

else

include $(TOP)/config/CONFIG_APP
buildInstall:: createLink
include $(TOP)/config/RULES_ARCHS
createLink:
	@if [ ! -d $(TOP)/data ]; then ln -s `pwd` $(TOP)/data; fi

endif
