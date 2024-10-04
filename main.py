import customtkinter as ctk
from ui import ClientApp
import click

@click.command()
@click.option('--host', '-h', default="212.193.27.248", help='Host ip.')
@click.option('--port', '-p', default="443", help='Host port')
def setup(host, port):

    print(f"Host: {host}, Port: {port}")

    root = ctk.CTk()
    app = ClientApp(root, host, port)
    root.mainloop()

if __name__ == "__main__":
    setup()
