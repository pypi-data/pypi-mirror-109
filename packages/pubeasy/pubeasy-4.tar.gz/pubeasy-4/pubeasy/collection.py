from .pubeasy import MakeFigure



class Collection(object):

  def __init__(self,**argv):


      self.figs = {}

  def add_figure(self,name):

      self.figs.update({name:MakeFigure()})

      return self.figs[name]

  def finalize(self,name,**argv):

      self.figs[name].finalize(**argv)



