from tkinter import *

ws = Tk()
ws.title('PythonGuides')


img = PhotoImage(file='wykres.png')
Label(ws, image=img).grid()

ws.mainloop()