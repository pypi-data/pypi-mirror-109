import pyecharts
from pyecharts.charts import *


def line(xais=list,yais=list,name=str,filename=str):
        
    bar = Line()
    bar.add_xaxis(xais)
    bar.add_yaxis(name,yais)
    bar.render(filename+".html")
def bar(xais=list,yais=list,name=str,filename=str):
        
    bar2 = Bar()
    bar2.add_xaxis(xais)
    bar2.add_yaxis(name,yais)
    bar2.render(filename+".html")



