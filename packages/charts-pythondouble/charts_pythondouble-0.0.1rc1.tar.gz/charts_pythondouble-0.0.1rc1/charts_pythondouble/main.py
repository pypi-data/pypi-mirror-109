class Pycharts:
    def __init__(self):
        import pyecharts
        from pyecharts.charts import *
    def line(self,xais=list,yais=list,name=str,filename=str):
        import pyecharts
        from pyecharts.charts import *
        bar = Line()
        bar.add_xaxis(xais)
        bar.add_yaxis(name,yais)
        bar.render(filename+".html")

