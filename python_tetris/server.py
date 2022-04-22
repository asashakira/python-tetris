import pickle
import socket
import threading

from .tetris import Tetris

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (SERVER, PORT)

players = [Tetris(0, 200), Tetris(350, 200)]


def handle_client(conn, addr, player):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(1048576))
            players[player] = data

            if not data:
                break

            reply = players[0] if player == 1 else players[1]

            conn.sendall(pickle.dumps(reply))
        except Exception:
            break

    print(f"[DISCONNECTED] {addr} disconnected.")
    conn.close()


current_player = 0
print("[STARTING] server is starting...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDR)
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER} {PORT}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, current_player)
        )
        thread.start()
        current_player += 1
        current_player %= 2
