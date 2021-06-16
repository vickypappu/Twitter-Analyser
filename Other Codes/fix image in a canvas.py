from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  
canvas = Canvas(root, width = 300, height = 300)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("first_review.png"))  
canvas.create_image(20, 20, anchor=NW, image=img) 
root.mainloop()
