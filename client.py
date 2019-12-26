import socket
from DH import Endpoint

HOST = '127.0.0.1'
PORT = 8082

sock = socket.socket()
sock.connect((HOST, PORT))


clientDH = Endpoint()
clientDH.bunch_of_public_keys()

keys = str(clientDH.client_public_key)+' '+str(clientDH.server_public_key)
sock.send(keys.encode())


msg = sock.recv(1024).decode()
if msg == "Access is allowed":
    print(msg+"\nTo exit, send \"exit\"")

    
    server_key_partial = int(sock.recv(1024).decode())
    


    client_partial_key = clientDH.generate_partial_key()
    sock.send(str(client_partial_key).encode())  

    
    clientDH.generate_full_key(server_key_partial)

    while True:
        msg = input(""">>""")
        if msg == 'exit' or msg == 'Exit':
            sock.send(clientDH.encrypt_message(msg).encode())
            break
        
        sock.send(clientDH.encrypt_message(msg).encode())


    sock.close()

else:
    print("Access not allowed")
    sock.close()
