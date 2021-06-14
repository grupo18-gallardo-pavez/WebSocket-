import socket
import threading

HEADER = 64
PORT = 3074
SERVER = '158.251.91.68'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
MAC= '30:9C:23:6A:78:79'  #MAC asociadas
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #asociacion al socket
server.bind(ADDR)

def handle_client(conn, addr):
    cont = 1
    print(f"[NEW CONECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if ((msg != MAC) and (cont == 1)):
                print("ERROR, MAC Incorrecta")
                conn.send("ERROR, MAC Incorrecta".encode(FORMAT))
                connected = False
            if ((msg == MAC) and (cont == 1)):
                print("CONECTADO, MAC Correcta")
                cont += 1
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}]{msg}")
            conn.send("Mensaje recibido".encode(FORMAT))
    conn.close()
#---------------Receptor de clientes-------------------------------
def start():
    server.listen()
    print(f"[LISTEN] server is linstening on addres {ADDR}")
    while True:
        conn , addr = server.accept()
        thread = threading.Thread(target = handle_client, args= (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
print("[STARTING] Sever is running")
start()
