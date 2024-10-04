import asyncio
import websockets
import socket

async def listen_to_server(app):
    url = f"ws://{app.host}:{app.port}/websockets/ws/{socket.gethostname()}"
    async with websockets.connect(url) as websocket:
        app.websocket = websocket
        try:
            while True:
                message = await websocket.recv()
                await app.control(message)
        except websockets.ConnectionClosed:
            print("Connection closed")

async def send_message(app, message):
    if app.websocket:
        try:
            await app.websocket.send(message)
        except websockets.ConnectionClosed:
            print("Connection is closed")
    else:
        print("WebSocket is not connected")


def start_websocket_connection(app):
    asyncio.run(listen_to_server(app))
