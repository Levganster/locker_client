import tkinter as tk

def disable_event():
    pass

root = tk.Tk()

# root.attributes('-fullscreen', True)
root.attributes('-topmost',True)
root.protocol("WM_DELETE_WINDOW", disable_event)

root.resizable(True, True) #False, False

root.mainloop()