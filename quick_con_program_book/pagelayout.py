from pylatex import Package
from pylatex.base_classes import BaseLaTeXNamedContainer

class Landscape(BaseLaTeXNamedContainer):
    def __init__(self, **kwargs):
        BaseLaTeXNamedContainer.__init__(self, 'landscape', packages=[Package('pdflscape')],**kwargs)
    

class Multicols(BaseLaTeXNamedContainer):
    def __init__(self,number_of_columns=2, **kwargs):
        argument=str(number_of_columns)
        BaseLaTeXNamedContainer.__init__(self, 'multicols', argument=argument, packages=[Package('multicol')],**kwargs)
        
