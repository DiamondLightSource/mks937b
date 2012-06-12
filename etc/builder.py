from iocbuilder import SetSimulation, AutoSubstitution, Substitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol

class mks937b(AutoSubstitution, AutoProtocol):
    TemplateFile = 'mks937b.template'
    ProtocolFiles = ['mks937b.protocol']
    
    def __init__(self, address, **args):
        # make sure address is a 3 digit int
        args['address'] = "%03d" % int(address)
        self.__super.__init__(**args)        

class _mks937bImg_template(AutoSubstitution):
    TemplateFile = 'mks937bImg.template'

class _mks937bPirg_template(AutoSubstitution):
    TemplateFile = 'mks937bPirg.template'

class mks937bImgorPirg:
    pass

class mks937bImg(_mks937bImg_template, mks937bImgorPirg):
    def __init__(self, GCTLR, **args):
        # get port and addr from GCTLR
        args['port'] = GCTLR.args['port']
        args['address'] = GCTLR.args['address']
        self.__super.__init__(**args)

    # construct the ArgInfo
    ArgInfo = makeArgInfo(__init__,
        GCTLR = Ident('Parent mks937b object', mks937b)) + \
        _mks937bImg_template.ArgInfo.filtered(without = ('port', 'address'))
        

class mks937bPirg(_mks937bPirg_template, mks937bImgorPirg):
    def __init__(self, GCTLR, **args):
        # get port from GCTLR
        args['port'] = GCTLR.args['port']
        args['address'] = GCTLR.args['address']
        self.__super.__init__(**args)

    # construct the ArgInfo
    ArgInfo = makeArgInfo(__init__,
        GCTLR = Ident('Parent mks937b object', mks937b)) + \
        _mks937bPirg_template.ArgInfo.filtered(without = ('port', 'address'))

class _mks937bRelays_template(AutoSubstitution):
    TemplateFile = 'mks937bRelays.template'
    
class mks937bRelays(_mks937bRelays_template):
    relays = {}
    def __init__(self, GAUGE, **args):
        # get port from GAUGE
        self.relays.setdefault(GAUGE, []).append(0)
        args['port'] = GAUGE.args['port']
        args['address'] = GAUGE.args['address']
        args['device'] = GAUGE.args['device'] + ":RLY%d" % len(self.relays[GAUGE])
        self.__super.__init__(**args)

    # construct the ArgInfo
    ArgInfo = makeArgInfo(__init__,
        GAUGE = Ident('Parent mks937bPirg or mks937bImg object', mks937bImgorPirg)) + \
        _mks937bRelays_template.ArgInfo.filtered(without = ('port', 'address', 'device'))

class mks937bGauge(AutoSubstitution):
    def __init__(self, id, **args):
        # make sure the id is a 2 digit int
        args['id'] = "%02d" % int(id)
        self.__super.__init__(**args)

    TemplateFile = 'mks937bGauge.template'

class mks937bHy8401(AutoSubstitution):
    TemplateFile = 'mks937bHy8401.template'

# The following create groups that can be used in vacuum spaces
class mks937bGaugeGroup(AutoSubstitution):
    TemplateFile = 'mks937bGaugeGroup.template'

class mks937bImgGroup(AutoSubstitution):
    TemplateFile = 'mks937bImgGroup.template'

class mks937bPirgGroup(AutoSubstitution):
    TemplateFile = 'mks937bPirgGroup.template'

class mks937bImgDummy(AutoSubstitution):
    TemplateFile = 'mks937bImgDummy.template'

