import random
import socket
from DH import Endpoint

HOST = '127.0.0.1'
PORT = 8082

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()
print(f'Listen {PORT} port...')

def make_keys(conn):
    
    
    bunch = conn.recv(2054).decode()
    bunch = bunch.split(' ')
    
    serverDH = Endpoint(int(bunch[0]), int(bunch[1]), random.randint(1, 320))
    return serverDH

def access_check(client_public_key):
    
    with open('Keys.txt', 'r') as file:
        flag = False
        for line in file:
            if int(line) == client_public_key:
                flag = True
                break
    return flag

serverDH = make_keys(conn)

if access_check(serverDH.client_public_key):
    conn.send("Access is allowed".encode())

    
    server_partial_key = serverDH.generate_partial_key()
    conn.send(str(server_partial_key).encode())

    
    client_key_partial = int(conn.recv(1024).decode())
    print(client_key_partial)

    
    serverDH.generate_full_key(client_key_partial)


    while True:

        
        msg = conn.recv(2024).decode()
        print(f'Encrypt messege: {msg} \nDecrypt messege: {serverDH.decrypt_message(msg)}\n')
        if serverDH.decrypt_message(msg) == 'Exit' or serverDH.decrypt_message(msg) == 'exit':
            break

    conn.close()

else:
    conn.close()
