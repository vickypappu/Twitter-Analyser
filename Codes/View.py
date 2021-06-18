import sys 
import pandas as pd
from tkinter import Text,Tk,END

def Viewtweets(df):
    root = Tk() 
    t1 = Text(root) 
    t1.pack()
    class PrintToT1(object): 
     def write(self, s): 
         t1.insert(END, s) 
    sys.stdout = PrintToT1() 
    print (df)
    sys.stdout = sys.__stdout__
    root.mainloop() 

if __name__ == "__main__":
    import numpy as np
    dates = pd.date_range('20160101', periods=6)
    df1 = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
    Viewtweets(df1)
