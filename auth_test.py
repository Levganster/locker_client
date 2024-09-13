import json
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import asyncio
import websockets
from PIL import Image
from pystray import Icon, MenuItem, Menu

# from comands import control

# Функция для отправки авторизационных данных на API
def authenticate(username, password):
    url = "http://192.168.111.169:8000/auth/token"  # URL твоего API
    payload = {"username": username, "password": password}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()  # Возвращаем True и токен
        else:
            return False, response.text  # Возвращаем ошибку
    except Exception as e:
        return False, str(e)
    

show = True
hide = False

def disable_event():
    pass

# Класс для клиентского приложения
class ClientApp:
    def __init__(self, root):

        
        # Запускаем WebSocket-подключение в отдельном потоке
        websocket_thread = threading.Thread(target=self.start_websocket_connection, daemon=True)
        websocket_thread.start()


        self.root = root
        
        root.attributes('-fullscreen', True)
        self.root.attributes('-topmost',True)
        self.root.protocol("WM_DELETE_WINDOW", disable_event)
        self.root.resizable(True, True) #False, False

        self.root.title("Авторизация")

        self.username_label = tk.Label(root, text="Имя пользователя")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Пароль")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Войти", command=self.login)
        self.login_button.pack(pady=20)

        self.token = None

        # Иконка для системного трея
        self.icon = None #Image.open("icon.png")  # Путь к твоей иконке для трея
        self.tray_icon = None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, result = authenticate(username, password)
        if success:
            print(result.get('access_token')) # Пишем токен в консоль
            self.token = result.get('access_token')  # Сохраняем токен
            messagebox.showinfo("Успешно", "Вы вошли в систему!")
            global hide, show
            hide = True
            show = False
            self.hide_to_tray()
        else:
            messagebox.showerror("Ошибка", f"Ошибка авторизации: {result}")

    def hide_to_tray(self):
        # Сворачиваем окно
        self.root.withdraw()

        # Создаем иконку для трея
        self.tray_icon = Icon("ClientApp", self.icon)
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

    def show_window(self):
        # Показываем окно и закрываем трей
        self.root.deiconify()
        if self.tray_icon:
            self.tray_icon.stop()

    def exit_app(self, icon=None, item=None):
        # Закрываем приложение
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    async def listen_to_server(self):
        url = "ws://192.168.111.169:8000/websockets/ws"  # URL WebSocket-соединения
        async with websockets.connect(url) as websocket:
            while True:
                try:
                    message = await websocket.recv()  # Получаем сообщения от сервера
                    print(f"Сообщение от сервера: {message}")
                    # Обработка команды из сообщения
                    self.handle_message(message)
                except websockets.ConnectionClosed:
                    print("Соединение с сервером разорвано")
                    break

    def start_websocket_connection(self):
        # Запускаем асинхронное WebSocket-соединение
        asyncio.run(self.listen_to_server())

    def handle_message(self, message):
            """
            Обрабатываем сообщение от сервера.
            Предполагаем, что сообщение в формате JSON и содержит ключ 'command_code'.
            """
            try:
                data = json.loads(message)
                comand_code = data  # Извлекаем код команды
                if comand_code is not None:
                    self.control(comand_code)  # Вызываем функцию control
            except json.JSONDecodeError:
                print("Ошибка при декодировании сообщения")

    def control(self, comand_code):
        global hide, show
        if not hide and comand_code == 1:
            hide = True
            show = False
            self.hide_to_tray()
        if not show and comand_code == 2:
            hide = False
            show =True
            self.show_window()
        if comand_code == 3:
            self.exit_app()
        
        print(hide, show)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)

    root.mainloop()
