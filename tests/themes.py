from tkinter import *

from tkinter import ttk

# Create GUI window
window = Tk()

window.title("Delftstack")
window.geometry("500x400")
# create style object
style = ttk.Style(window)


def theme_changer():
    # Change  theme
    style.theme_use(window.selected_theme.get())


label = ttk.Label(window, text="Name:")
label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

entry = ttk.Entry(window)
entry.grid(column=1, row=0, padx=10, pady=10, sticky="w")

button = ttk.Button(window, text="press")
button.grid(column=2, row=0, padx=10, pady=10, sticky="w")

window.selected_theme = StringVar()
theme_frame = ttk.LabelFrame(window, text="Themes")
theme_frame.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky="w")

for theme_name in style.theme_names():
    # Create a bulk of radio buttons using loop
    radio_buttons = ttk.Radiobutton(
        theme_frame,
        text=theme_name,
        value=theme_name,
        variable=window.selected_theme,
        command=theme_changer,
    )
    radio_buttons.pack(expand=True, fill="both")

window.mainloop()

print(style.theme_names())