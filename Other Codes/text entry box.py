#Imports all (*) classes,
#atributes, and methods of tkinter into the
#current workspace

from tkinter import *

def getvalue():
    print(mystring.get())

root = Tk()
root.title('how to get text from textbox')


mystring = StringVar()






Entry(root, textvariable = mystring).grid(row=0, column=1, sticky=E) #entry textbox

WSignUp = Button(root, text="print text", command=getvalue).grid(row=3, column=0, sticky=W) #button


root.mainloop()
