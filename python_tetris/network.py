import pickle
import socket


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.host, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(1048576))
        except Exception:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(1048576))
        except socket.error as e:
            print(e)
