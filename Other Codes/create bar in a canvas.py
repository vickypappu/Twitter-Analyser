# drawing a bar graph with the Tkinter canvas and
# canvas.create_rectangle(x0, y0, x1, y1, option, ...)
# note: coordinates are relative to the top left corner of the canvas
# used a more modern import to give Tkinter items a namespace
# tested with Python24  by    vegaseat    01nov2006

import tkinter as tk  # gives tk namespace

#data = [20, 15, 10, 7, 5, 4, 3, 2, 1, 1, 0]

values = [8, 21, 21]
data = values
root = tk.Tk()
root.title("Tkinter Bar Graph")
c_width = 400
c_height = 350
c = tk.Canvas(root, width=c_width, height=c_height, bg= 'white')
c.pack()

# the variables below size the bar graph
# experiment with them to fit your needs
# highest y = max_data_value * y_stretch
y_stretch = 15
# gap between lower canvas edge and x axis
y_gap = 20
# stretch enough to get all data items in
x_stretch = 10
x_width = 20
# gap between left canvas edge and y axis
x_gap = 20


for x, y in enumerate(data):
    # calculate reactangle coordinates (integers) for each bar
    x0 = x * x_stretch + x * x_width + x_gap
    y0 = c_height - (y * y_stretch + y_gap)
    x1 = x * x_stretch + x * x_width + x_width + x_gap
    y1 = c_height - y_gap
    # draw the bar
    c.create_rectangle(x0, y0, x1, y1, fill="red")
    # put the y value above each bar
    c.create_text(x0+2, y0, anchor=tk.SW, text=str(y))
    c.create_text(x1-17, y1+15, anchor=tk.SW, text=str(y))
    

root.mainloop()
 
