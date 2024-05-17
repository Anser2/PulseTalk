import socket
import threading
import sqlite3
import os
import time

os.makedirs('files', exist_ok=True)

conn = sqlite3.connect('contacts.db', check_same_thread=False)
c = conn.cursor()

c.execute("""DROP TABLE IF EXISTS contacts""")
c.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        username TEXT PRIMARY KEY,
        password TEXT,
        ip_address TEXT,
        port INTEGER
     )
""")
table_values= c.execute("SELECT * FROM contacts").fetchall()
print("Contacts:")
print(table_values)



c.execute("""CREATE TABLE IF NOT EXISTS blocked_users (
           username TEXT,
           blocked_username TEXT
          )
""")
cursed_users = c.execute("SELECT * FROM blocked_users").fetchall()
print("CURSED USERS:")
print(cursed_users)


BLOCKED_USERS = c.execute("SELECT blocked_username FROM blocked_users").fetchall()

def block_user_func(username, blocked_username):
    c.execute("INSERT INTO blocked_users VALUES (?, ?)", (username, blocked_username))
    conn.commit()
    if blocked_username in client_sockets:
        client_sockets[blocked_username].send("You have been blocked.".encode())
        client_sockets[blocked_username].close()

def handle_upload(client_socket):
    filename = client_socket.recv(1024).decode()
    file_data = client_socket.recv(1024)
    with open(os.path.join('files', filename), 'wb') as f:
        f.write(file_data)

def handle_download(client_socket):
    filename = client_socket.recv(1024).decode()
    with open(os.path.join('files', filename), 'rb') as f:
        client_socket.sendall(f.read())

def add_contact(username, password, client_address):
    ip_address, port = client_address
    c.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (username, password, ip_address, port))

def authenticate(username, password):
    c.execute("SELECT * FROM contacts WHERE username = ? AND password = ?", (username, password))
    return c.fetchone() is not None

def update_ip_address(username, ip_address):
    c.execute("UPDATE contacts SET ip_address = ? WHERE username = ?", (ip_address, username))
    conn.commit()

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        data = client_socket.recv(1024)
        username, password = data.decode().split(',')

        if authenticate(username, password):
            update_ip_address(username, client_address)
        else:
            add_contact(username, password, client_address)

        client_sockets[username] = client_socket
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            if data.startswith(b'block,'):
                blocked_username = data.decode().split(',')[1]
                block_user_func(username, blocked_username)
            elif data == b'upload':
                handle_upload(client_socket)
            elif data == b'download':
                handle_download(client_socket)
            else:
                recipient_message = data.decode().split(',', 1)
                if len(recipient_message) == 2:
                    recipient, message = recipient_message
                    if recipient in BLOCKED_USERS:
                        client_socket.send("The user is blocked cannot send message.".encode())
                    else:
                        send_to_user(recipient, f"{username}: {message}".encode())
                else:
                    print(f"{client_address} broadcasted: ")
                    broadcast(data)

            print(f"Received message from {client_address}: {data.decode()}")
    except ConnectionResetError:
        print(f"Connection with {client_address} was closed unexpectedly.")
    finally:
        print(f"Connection from {client_address} closed.")
        client_socket.close()
        if username in client_sockets:
            del client_sockets[username]

def broadcast(message):
    for client in client_sockets.values():
        client.send(message)

client_sockets = {}

def send_to_user(username, message):
    if username in client_sockets:
        blocked_users = [u[0] for u in c.execute("SELECT blocked_username FROM blocked_users WHERE username = ?", (username,)).fetchall()]
        sender = message.decode().split(':')[0]
        if sender not in blocked_users:
            client_sockets[username].send(message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)

print("Server started, listening on port 5555")

while True:
    client_socket, client_address = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
