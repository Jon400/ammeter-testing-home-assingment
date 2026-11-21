"""
Base TCP client implementation
"""

import socket


class BaseTCPClient:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.timeout = timeout  # seconds to wait for the connection and for each reply
        self.socket = None

    def connect(self):
        """Establish a TCP connection to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))

    def send(self, data: bytes):
        """Send data to the server."""
        if not self.socket:
            raise ConnectionError(f"Not connected to {self.host}:{self.port}; call connect() first")
        self.socket.sendall(data)

    def receive(self, buffer_size: int = 1024) -> bytes:
        """Receive data from the server."""
        if not self.socket:
            raise ConnectionError(f"Not connected to {self.host}:{self.port}; call connect() first")
        return self.socket.recv(buffer_size)

    def close(self):
        """Close the TCP connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
