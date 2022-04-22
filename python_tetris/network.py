from __future__ import annotations

import pickle
import socket
from typing import Any


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.host, self.port)
        self.p = self.connect()

    def get_p(self) -> Any | None:
        return self.p

    def connect(self) -> Any | None:
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(1048576))
        except Exception:
            pass
        return None

    def send(self, data: Any) -> Any | None:
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(1048576))
        except socket.error as e:
            print(e)
        return None
