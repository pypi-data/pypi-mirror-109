import pyecharts
from pyecharts.charts import *
class Pycharts:
    def __init__(self):
        pass
    def line(self,xais=list,yais=list,name=str,filename=str):
        
        bar = Line()
        bar.add_xaxis(xais)
        bar.add_yaxis(name,yais)
        bar.render(filename+".html")

