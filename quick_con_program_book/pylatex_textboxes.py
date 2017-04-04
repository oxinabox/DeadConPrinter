import pylatex.base_classes.command
def patched_commandbase_eq(self,other): #MONKEY-PATCH
    if isinstance(other, CommandBase):
        return self._CommandBase__key() == other._CommandBase__key()
    return False
pylatex.base_classes.command.CommandBase.__eq__=patched_commandbase_eq

from pylatex.base_classes import *
from pylatex.base_classes.command import Command,Arguments
from pylatex import Package

class TcboxFit(Command):  
    def __init__(self,arguments=None,options=None):
        packages = [Package('tcolorbox', options='fitting')]
        Command.__init__(self, "tcboxfit", arguments=arguments, options=options, packages=packages)

class FixedTextbox(LatexObject): #Hack: THis should be a container
    def __init__(self,text, hpos,vpos, height,width, tcb_options=None):
        self.text=text
        self.hpos=hpos
        self.vpos=vpos
        self.height=height
        self.width=width
        
        self.tcboxfit = TcboxFit(options=tcb_options, arguments=text)
        self.tcboxfit.options._key_value_args["height"]=height
        
        self.packages = [Package('textpos', options='absolute'),Package('tcolorbox', options='fitting')]
        LatexObject.__init__(self)
    
    def dumps(self): 
        return """
\\begin{textblock*}{%(width)s}(%(hpos)s, %(vpos)s)
    %(tcbox)s
\\end{textblock*}
        """ % {'width':self.width, 'hpos':self.hpos, 'vpos':self.vpos, 'tcbox':self.tcboxfit.dumps()}
    
class TextcolorboxStyle(LatexObject):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs= kwargs
        self.packages = [Package('tcolorbox', options='fitting')]
        LatexObject.__init__(self)

    def dumps(self): 
        def express_arguments(args,kwargs):
            args_strs = list(map(str,args))
            kwargs_strs = ["%s=%s" % (k,v) for (k,v) in kwargs.items()]
            return ",".join(args_strs + kwargs_strs)
        return "\\tcbset{%s}" % express_arguments(self.args, self.kwargs)

def textpos_origin(x,y):
    return Command('textblockorigin',arguments=[x,y])