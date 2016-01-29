from pylatex import Package
from pylatex.base_classes.containers import Environment

class Landscape(Environment):
    def __init__(self, **kwargs):
        self.packages=[Package('pdflscape')]
        Environment.__init__(self,**kwargs)
    

class Multicols(Environment):
    def __init__(self,number_of_columns=2, **kwargs):
        self.packages=[Package('multicol')]
        Environment.__init__(self, arguments=[str(number_of_columns)],**kwargs)
        
