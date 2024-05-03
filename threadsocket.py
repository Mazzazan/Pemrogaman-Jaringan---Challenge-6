import socket
import select
import sys
import threading
import re

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_client = []

def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                print(f"Received message from <{addr[0]}>: {message}")
                # Using regex to find operands and operator
                match = re.match(r"(\d+)([\+\-\*\/])(\d+)", message)
                if match:
                    num1 = int(match.group(1))
                    operator = match.group(2)
                    num2 = int(match.group(3))
                    result = None
                    if operator == '+':
                        result = num1 + num2
                    elif operator == '-':
                        result = num1 - num2
                    elif operator == '*':
                        result = num1 * num2
                    elif operator == '/':
                        result = num1 / num2  # Note: handle division by zero
                    
                    if result is not None:
                        client_msg = message + " = " + str(result)
                        message_to_send = client_msg.encode()
                        print(f"Sending result: {message_to_send.decode()}")
                        broadcast(message_to_send, conn)
                else:
                    print("Invalid message format.")
            else:
                remove(conn)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
        
def broadcast(message, connection):
    for clients in list_of_client:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
def remove(connection):
    if connection in list_of_client:
        list_of_client.remove(connection)
        
while True:
    conn, addr = server.accept()
    list_of_client.append(conn)
    print(addr[0] + " connected")
    threading.Thread(target=clientthread,args=(conn,addr)).start()
    
conn.close()