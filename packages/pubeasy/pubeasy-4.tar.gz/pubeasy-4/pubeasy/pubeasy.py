import matplotlib.font_manager as fm
from matplotlib.pylab import *
import os, sys
import warnings
import gzip,pickle

warnings.simplefilter("ignore")

LARGE = 22


class MakeFigure(object):
    def __init__(self, **argv):

        self.init_plotting(**argv)
        self.names = []
        self.colors = ['#1f77b4', '#f77f0e', '#2ca02c']

    def get_color(self, i):

        return self.colors[i]

    def load(self,datafile):

      with gzip.open(datafile + '.npz', 'rb') as f:
          return pickle.load(f)



    def savefigure(self,namefile=None,prefix = './'):

      if namefile == None:
       namefile =  prefix + sys.argv[0].split('.')[0]+'.png'
    
      namefile = prefix + sys.argv[0].split('.')[0] + '.png'

      savefig(namefile, dpi=500)

    def add_plot(self, x, y, marker=False, **argv):

        color = argv.setdefault('color', 'k')
        if 'name' in argv.keys():
            label = argv['name']
            if not label in self.names:
                self.names.append(label)
        else:
            self.names.append('_nolegend_')

        if argv.setdefault('model', 'plot') == 'plot':
            self.ax.plot(x,
                         y,
                         marker='o' if marker else 'None',
                         color=color,
                         linestyle=argv.setdefault('ls', '-'))
        elif argv.setdefault('model', 'plot') == 'scatter':
            self.ax.scatter(x,
                            y,
                            marker=argv.setdefault('marker', 'o'),
                            c=color)
        elif argv.setdefault('model', 'plot') == 'fill':
            self.ax.fill_between(x, np.zeros_like(x), y, color=color)
        elif argv.setdefault('model', 'plot') == 'hist':
            self.ax.hist(x, argv['n_bins'], color=color, alpha=argv['alpha'])

    def add_labels(self, x, y):

        f = self.fonts['regular']
        f.set_size(LARGE)
        self.ax.set_xlabel(x, fontproperties=self.fonts['regular'])
        self.ax.set_ylabel(y, fontproperties=self.fonts['regular'])

    def finalize(self, **argv):

       f = self.fonts['regular']
       f.set_size(18)
       if len(self.names) > 0:
            #legend(self.names,prop=f,frameon=True,bbox_to_anchor=(0.8, 0.48, 0.2, 0.2))
            legend(self.names, prop=f, frameon=True, ncol=1, loc=0)
       xticks(fontproperties=self.fonts['regular'])
       yticks(fontproperties=self.fonts['regular'])

       f = self.fonts['regular']
       f.set_size(18)
       if len(self.names) > 0:
            #if not '_nolegend_' in self.names: 
            legend(self.names,prop=f,frameon=True,ncol=1,loc=argv.setdefault('loc_legend',1),facecolor='w')
       xticks(fontproperties=self.fonts['regular'])
       yticks(fontproperties=self.fonts['regular'])


       for child in self.ax.get_children(): 
        x = isinstance(child, matplotlib.text.Text)
        if x:
         child.set_font_propertie = self.fonts['regular']
       for child in gcf().get_children(): 
        x = isinstance(child, matplotlib.text.Text)
        if x:
         child.set_font_properties = self.fonts['regular']

       if argv.setdefault('grid', False):
            grid('on', which='both')

       for child in gca().get_children():
            x = isinstance(child, matplotlib.text.Text)
            if x:
                child.set_font_propertie = self.fonts['regular']
       for child in gcf().get_children():
            x = isinstance(child, matplotlib.text.Text)
            if x:
                child.set_font_properties = self.fonts['regular']

       for label in gca().get_xticklabels():
            label.set_fontproperties(self.fonts['regular'])
       for label in gca().get_yticklabels():
            label.set_fontproperties(self.fonts['regular'])

       xscale(argv.setdefault('xscale', 'linear'))

       if 'xlim' in argv.keys():
            xlim(argv['xlim'])
       if 'ylim' in argv.keys():
            ylim(argv['ylim'])

       yscale(argv.setdefault('yscale', 'linear'))

       if argv.setdefault('write',False):
          self.savefigure(argv.setdefault('namefile',None)) 
       
       if argv.setdefault('show',True):
           
        show()
      
    #-------------------


    def init_plotting(self,extra_x_padding = 0.0,extra_y_padding=0.0,extra_bottom_padding = 0.02,extra_top_padding=  0.0,paraview=False,shape='horizontal',delta_square = 0,presentation=False,extra_right_padding=0):


     rcParams['xtick.major.pad']='10'
     rcParams['mathtext.fontset'] = 'cm'
     rcParams['lines.linewidth'] = 3
     rcParams['font.size'] = LARGE
     rcParams['xtick.labelsize'] = LARGE
     rcParams['ytick.labelsize'] = LARGE
     if shape == 'horizontal':
      rcParams['figure.figsize'] = [8.0, 5.0]
     if shape == 'square' : 
      rcParams['figure.figsize'] = [4.0, 4.0]
     if shape=='vertical':
      rcParams['figure.figsize'] = [5, 6]
 

     #load fonts----
     filename = os.path.dirname(__file__) + '/fonts/cmunrm.ttf'
     prop_regular = fm.FontProperties(fname=filename,family='serif')
     filename = os.path.dirname(__file__) + '/fonts/cmunbx.ttf'
     prop_bold = fm.FontProperties(fname=filename,family='serif')
     filename = os.path.dirname(__file__) + '/fonts/cmunti.ttf'
     prop_italic = fm.FontProperties(fname=filename,family='serif')
     fonts = {'regular':prop_regular,'italic':prop_italic,'bold':prop_bold}

     rcParams['figure.dpi'] = 80
     rcParams['savefig.dpi'] = 400
     rcParams['xtick.major.size'] = 3
     rcParams['xtick.minor.size'] = 3
     rcParams['figure.edgecolor'] = 'k'
     rcParams['figure.facecolor'] = 'w'
     rcParams['xtick.major.width'] = 1
     rcParams['xtick.minor.width'] = 1
     rcParams['ytick.major.size'] = 3
     rcParams['ytick.minor.size'] = 3
     rcParams['ytick.major.width'] = 1
     rcParams['ytick.minor.width'] = 1
     rcParams['legend.frameon'] = False
     rcParams['legend.fontsize'] = 25
     rcParams['axes.linewidth'] = 1

     self.ax = axes([0.12+extra_x_padding,0.15+extra_bottom_padding,0.78-extra_x_padding-extra_right_padding,0.75-extra_bottom_padding-extra_top_padding])
     self.fonts = fonts

