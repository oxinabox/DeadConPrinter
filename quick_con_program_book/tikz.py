from pylatex.base_classes import BaseLaTeXNamedContainer, BaseLaTeXClass
from pylatex.parameters import Options

class Tikz (BaseLaTeXNamedContainer):
    """Enumerate class for numbered list """
    def __init__(self, options=None, argument=None, **kwargs):
        """
        :param options:
        :param argument:
        :type name: str
        :type options: str or list or :class:`parameters.Options` instance
        :type argument: str
        """
        packages = [Package('tikz')]
        BaseLaTeXNamedContainer.__init__(self,'tikzpicture', options, argument, packages=packages, **kwargs)
        
        


class At(BaseLaTeXClass):
    def __init__(self,*args):
        self.loc=args
        
        packages = [Package('tikz')]
        BaseLaTeXClass.__init__(self,packages)
    
    def dumps(self):
        if len(self.loc)>0:
            return ' at (%s) ' % ','.join(map(str,self.loc))
        else:
            return ''
    
class Node(Command):
    """
    Eg:
        Node(arguments = ["Blah"],
             at = (2, 2),
             options=Options(entry.name, 
                         **{'minimum height': '4cm',
                             'text width':2cm})
                            )
    """
    
    def __init__(self, arguments=None, options=None, at=None):
        if at is None:
            self.at = At()
        elif isinstance(at,At):
            self.at=at
        else:
            self.at=At(*at)
            
        packages = [Package('tikz')]
        Command.__init__(self, 'node', arguments=arguments, options=options, packages=packages)
        
    def dumps(self):
        return '\\node{options}{at}{arguments};\n'.\
            format(options=self.options.dumps(),
                   at=self.at.dumps(),
                   arguments=self.arguments.dumps())
        
class TikzStyle(BaseLaTeXClass):
    """
    Eg: 
    entry = TikzStyle('session','draw','rectangle', 
                            align='center', anchor='north west',
                            **{'line width':'0.4pt'})
    """
    def __init__(self, name, *args, **kwargs):
        packages = [Package('tikz')]
        self.name=name
        self.args = args
        self.kwargs = kwargs
        BaseLaTeXClass.__init__(self, packages)
    
    @property
    def arg_strings(self):
        return list(map(str,self.args))
    
    @property
    def kwarg_strings(self):
        return ["%s = %s" % (k,v) for (k,v) in self.kwargs.items()]
    
    def dumps(self):
        settings = ",\n\t".join(self.arg_strings + self.kwarg_strings)
        return '\\tikzstyle{%s} = [\n\t%s\n]\n' % (self.name, settings)

