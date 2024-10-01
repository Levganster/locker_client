import customtkinter as ctk
from ui import ClientApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = ClientApp(root)
    root.mainloop()