import json
import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
import asyncio
import websockets
import socket
from PIL import Image
from pystray import Icon

# Function to send authentication data to the API
def authenticate(username, password):
    url = "http://212.193.27.248:8000/auth/token"  # URL of your API
    payload = {"username": username, "password": password}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()  # Return True and the token
        else:
            return False, response.text  # Return error
    except Exception as e:
        return False, str(e)

show = True
hide = False

def disable_event():
    pass

# Client application class
class ClientApp:
    def __init__(self, root):
        # Set up CustomTkinter
        ctk.set_appearance_mode("dark")  # Theme (dark/light)
        ctk.set_default_color_theme("blue")  # Color scheme

        self.root = root
        self.root.title("Authorization")

        # Set full-screen mode
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", disable_event)

        # Load the background image using CTkImage
        self.background_image = ctk.CTkImage(Image.open("background.jpg"), size=(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        # Add the background image
        self.background_label = ctk.CTkLabel(root, image=self.background_image, text="")
        self.background_label.place(relwidth=1, relheight=1)

        # Add CustomTkinter widgets and scale them
        self.frame = ctk.CTkFrame(root, width=400, height=350)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.upper_lable = ctk.CTkLabel(self.frame, text="")
        self.upper_lable.pack()
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

        # Icon for system tray
        self.icon = None  # Path to your tray icon
        self.tray_icon = None

        # Start WebSocket connection in a separate thread
        websocket_thread = threading.Thread(target=self.start_websocket_connection, daemon=True)
        websocket_thread.start()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, result = authenticate(username, password)
        if success:
            print(result.get('access_token'))  # Print the token to the console
            self.token = result.get('access_token')  # Save the token
            messagebox.showinfo("Success", "Logged in successfully!")
            global hide, show
            hide = True
            show = False
            self.hide_to_tray()
        else:
            messagebox.showerror("Error", f"Authorization error: {result}")

    def hide_to_tray(self):
        # Minimize the window
        self.root.withdraw()

        # Create an icon for the tray
        self.tray_icon = Icon("ClientApp", self.icon)
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

    def show_window(self):
        # Show the window and close the tray
        self.root.deiconify()
        if self.tray_icon:
            self.tray_icon.stop()

    def exit_app(self, icon=None, item=None):
        # Close the application
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    async def listen_to_server(self):
        url = f"ws://212.193.27.248:8000/websockets/ws/"  # WebSocket URL
        print(url)
        async with websockets.connect(url) as websocket:
            while True:
                try:
                    message = await websocket.recv()  # Receive messages from the server
                    print(f"Message from server: {message}")
                    # Handle the command from the message
                    self.handle_message(message)
                except websockets.ConnectionClosed:
                    print("Connection to the server closed")
                    break

    def start_websocket_connection(self):
        # Start an asynchronous WebSocket connection
        asyncio.run(self.listen_to_server())

    def handle_message(self, message):
        """
        Handle a message from the server.
        Assume the message is in JSON format and contains a 'command_code' key.
        """
        try:
            data = json.loads(message)
            comand_code = data  # Extract the command code
            if comand_code is not None:
                self.control(comand_code)  # Call the control function
        except json.JSONDecodeError:
            print("Error decoding message")

    def control(self, comand_code):
        global hide, show
        if not hide and comand_code == 1:
            hide = True
            show = False
            self.hide_to_tray()
        if not show and comand_code == 2:
            hide = False
            show = True
            self.show_window()
        if comand_code == 3:
            self.exit_app()


# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = ClientApp(root)

    root.mainloop()
