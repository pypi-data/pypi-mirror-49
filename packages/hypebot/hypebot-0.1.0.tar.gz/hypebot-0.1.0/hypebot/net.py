"""
Net module to provide connector for talking to livesplit.server
"""
import socket

from hypebot import settings


class LiveSplitClient:
    def __init__(self):
        self.connect()

    def connect(self, host=settings.LIVESPLIT_HOST, port=settings.LIVESPLIT_PORT):
        """ Connect to livesplit.server with the given host.port """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((host, port))

    def post(self, msg):
        """ Send a request and receive the contents of a response """
        self.send(msg)
        return self.recv()

    def recv(self):
        """ Receive a message from the livesplit server """
        return self.socket.recv(1024).decode().strip()

    def send(self, msg):
        """ Send a message to the livesplit server """
        self.socket.send(msg.encode() + b"\r\n")
