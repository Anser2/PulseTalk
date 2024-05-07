import socket
import threading
import sqlite3
import os


# Create a directory for files if it doesn't exist
os.makedirs('files', exist_ok=True)

# SQLite database connection
conn = sqlite3.connect('contacts.db', check_same_thread=False)
c = conn.cursor()


# Create or initialize the contacts table
c.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        username TEXT PRIMARY KEY,
        password TEXT,
        ip_address TEXT,
        port INTEGER
     )
""")
def handle_upload(client_socket):
    # Receive the filename and file data from the client
    filename = client_socket.recv(1024).decode()
    file_data = client_socket.recv(1024)
     # Save the file to the server's file directory
    with open(os.path.join('files', filename), 'wb') as f:
        f.write(file_data)

def handle_download(client_socket):
    # Receive the filename from the client
    filename = client_socket.recv(1024).decode()
    
    # Send the file data back to the client
    with open(os.path.join('files', filename), 'rb') as f:
        client_socket.sendall(f.read())           

# Function to add a new contact
def add_contact(username, password, client_address):
    ip_address, port = client_address  # unpack the tuple
    c.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (username, password, ip_address, port))

# Function to authenticate a user
def authenticate(username, password):
    c.execute("SELECT * FROM contacts WHERE username = ? AND password = ?", (username, password))
    return c.fetchone() is not None

# Function to update a contact's IP address
def update_ip_address(username, ip_address):
    c.execute("UPDATE contacts SET ip_address = ? WHERE username = ?", (ip_address, username))
    conn.commit()

# Function to handle file uploads from clients
def handle_upload(client_socket):
    filename = client_socket.recv(1024).decode()
    file_data = client_socket.recv(1024)
    
    with open(os.path.join('files', filename), 'wb') as f:
        f.write(file_data)

# Function to handle file downloads to clients
def handle_download(client_socket):
    filename = client_socket.recv(1024).decode()
    
    with open(os.path.join('files', filename), 'rb') as f:
        client_socket.sendall(f.read())

# Function to handle communication with a client
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    
    try:
        # Receive the username and password from the client
        data = client_socket.recv(1024).decode()
        username, password = data.split(',')
        
        if authenticate(username, password):
            update_ip_address(username, client_address)
        else:
            add_contact(username, password, client_address)
        
        # Add the client socket to the dictionary
        client_sockets[username] = client_socket
        while True:
            data = client_socket.recv(1024)
            if data == b'upload':
                handle_upload(client_socket)
            elif data == b'download':
                handle_download(client_socket)
            elif b',' in data:
                recipient, message = data.decode().split(',',1)
                send_to_user(recipient, f"{username}: {message}".encode())
            else:
                broadcast(data)    
                
    
            if not data:
                break
            print(f"Received message from {client_address}: {data.decode()}")
    except ConnectionResetError:
        print(f"Connection with {client_address} was closed unexpectedly.")
    finally:
        print(f"Connection from {client_address} closed.")
        client_socket.close()

def broadcast(message):
    for client in clients:
        client.send(message)

#     for client in clients:
clients=[]
client_sockets = {}
def send_to_user(username, message):
    if username in client_sockets:
        client_sockets[username].send(message)
   



# Set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)

print("Server started, listening on port 5555")
table_values= c.execute("SELECT * FROM contacts").fetchall()
print(table_values)

while True:
    client_socket, client_address = server.accept()
    clients.append(client_socket)
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client , args=(client_socket, client_address))
    client_thread.start()

