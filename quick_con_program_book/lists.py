from pylatex.base_classes import BaseLaTeXNamedContainer
from pylatex.command import Command 

        

class Item(Command):
    """
    A class that represents an item command.
    Should be used via the additem method on a List class
    """
    def __init__(self, op1, op2=None):
        if op2 is None:
            option = None
            argument = op1
        else:
            argument = op2
            option = op1

        Command.__init__(self, "item", argument, option)
        
        
class Description (BaseLaTeXNamedContainer):
    """Describe class for keyword labels lists"""
    def __init__(self):
        """
        :param options:
        :param argument:
        :type name: str
        :type options: str or list or :class:`parameters.Options` instance
        :type argument: str
        """
        BaseLaTeXNamedContainer.__init__(self,'description')
    
    def additem(self, label, description):
        self.append(Item(label, description))
        
        

class Enumerate (BaseLaTeXNamedContainer):
    """Enumerate class for numbered list """
    def __init__(self, option=None, argument=None, **kwargs):
        """
        :param options:
        :param argument:
        :type name: str
        :type options: str or list or :class:`parameters.Options` instance
        :type argument: str
        """
        BaseLaTeXNamedContainer.__init__(self,'enumerate', option, argument, **kwargs)
    
    def additem(self, itemtext):
        self.append(Item(itemtext))     
        
class Itemize (BaseLaTeXNamedContainer):
    """Itemize class for bullet point list"""
    def __init__(self, option=None, argument=None, **kwargs):
        """
        :param options:
        :param argument:
        :type name: str
        :type options: str or list or :class:`parameters.Options` instance
        :type argument: str
        """
        BaseLaTeXNamedContainer.__init__(self,'itemize', option, argument, **kwargs)
    
    def additem(self,itemtext):
        self.append(Item(itemtext))  
