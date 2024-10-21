import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import jwt
import threading
from auth import authenticate
from pystray import Icon, MenuItem
import asyncio
from websocket_client import start_websocket_connection



class ClientApp:
    def __init__(self, root, host, port):
        self.websocket = None

        self.host = host
        self.port = port

        self.status = "show"

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Authorization")

        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

        self.path = os.environ['USERPROFILE'] + "\\Documents\\locker_client-main\\background.jpg"
        self.background_image = ctk.CTkImage(Image.open(self.path), size=(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        self.background_label = ctk.CTkLabel(root, image=self.background_image, text="")
        self.background_label.place(relwidth=1, relheight=1)

        self.frame = ctk.CTkFrame(root, width=400, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.username_label = ctk.CTkLabel(self.frame, text="Username", font=("Arial", int(14)))
        self.username_label.pack()
        self.username_entry = ctk.CTkEntry(self.frame, width=200, height=30)
        self.username_entry.pack(pady=int(20))

        self.password_label = ctk.CTkLabel(self.frame, text="Password", font=("Arial", int(14)))
        self.password_label.pack()
        self.password_entry = ctk.CTkEntry(self.frame, show="*", width=200, height=30)
        self.password_entry.pack(pady=int(10))

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login, width=200, height=40)
        self.login_button.pack(pady=int(10))

        self.inder_label = ctk.CTkLabel(self.frame, text="", width=350, height=40)
        self.inder_label.pack(expand="true")

        self.token = None

        websocket_thread = threading.Thread(target=start_websocket_connection, args=(self,), daemon=True)
        websocket_thread.start()

    def login(self):
        host = self.host
        port = self.port

        username = self.username_entry.get()
        password = self.password_entry.get()

        success, result = authenticate(username=username, password=password, host=host, port=port)
        if success:
            self.token = result.get('access_token')
            messagebox.showinfo("Success", "Logged in successfully!")
            group = jwt.decode(self.token, options={"verify_signature": False})['subject']['group']
            asyncio.run(self.send_message(f"username: {username}, group: {group}"))
            print(f"username: {username}, group: {group}")
            self.hide_to_tray()
            self.password_entry.delete(0, ctk.END)
        else:
            print(result)
            if result.get('detail'):
                messagebox.showerror("Error", result.get('detail'))
            else:
                messagebox.showerror("Error", result)

    def hide_to_tray(self):
        self.root.withdraw()

        menu = (MenuItem('Show', self.show_window), MenuItem('Exit', self.exit_app))
        self.tray_icon = Icon("ClientApp", menu=menu)

        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()
        self.status = "hide"

    def show_window(self):
        self.root.deiconify()
        if self.tray_icon:
            self.tray_icon.stop()

    def exit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    async def send_message(self, message):
        if self.websocket is not None:
            try:
                await self.websocket.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("WebSocket connection is not established.")

    async def control(self, comand_code):
        if self.status == "show" and comand_code == "1":
            self.status = "hide"
            self.hide_to_tray()
        if self.status == "hide" and comand_code == "2":
            self.status = "show"
            self.show_window()
        if comand_code == "3":
            await self.websocket.close(code=1000, reason="Normal Closure")
            self.exit_app()

    def disable_event(self):
        pass
