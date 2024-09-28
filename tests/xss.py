import time
import requests
import threading
import asyncio
import websockets
import socket

class ClientApp:
    def __init__(self):
        
        self.websocket = None
        websocket_thread = threading.Thread(target=self.start_websocket_connection, daemon=True)
        websocket_thread.start()
    async def listen_to_server(self):
        url = f"ws://212.193.27.248:443/websockets/ws/{socket.gethostname()}"  # WebSocket URL
        print(url)
        async with websockets.connect(url) as websocket:
            self.websocket = websocket
            try:
                while True:
                    try:
                        # Получение сообщений от сервера
                        message = await websocket.recv()
                        print(f"Message from server: {message}")
                        # Обработка полученного сообщения
                    except websockets.ConnectionClosed:
                        print("Connection to the server closed")
                        break
            except Exception as e:
                print(f"An error occurred: {e}")

    async def send_message(self, message):
        if self.websocket is not None:
            try:
                await self.websocket.send(message)
                print(f"Message sent to server: {message}")
            except websockets.ConnectionClosed:
                print("Cannot send message, connection is closed.")
        else:
            print("WebSocket connection is not established.")

    def start_websocket_connection(self):
        # Start an asynchronous WebSocket connection
        asyncio.run(self.listen_to_server())


if __name__ == "__main__":
    app = ClientApp()

    print(0)
    time.sleep(2)
    asyncio.run(app.send_message("username: <script>alert('132')</script>, group: 1"))
    print(1)
    time.sleep(10)