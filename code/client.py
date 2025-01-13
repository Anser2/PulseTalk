import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import ttk
import socket
import threading
import uuid

def select_file():
    filename = filedialog.askopenfilename()
    upload_entry.delete(0, tk.END)  # Clear the entry field
    upload_entry.insert(0, filename)  # Insert the selected filename

def upload_file(filename):
    if filename:
        client_socket.send('upload'.encode())
        with open(filename, 'rb') as f:
            file_data = f.read()
        client_socket.send(filename.encode())
        client_socket.send(file_data)
        download_entry.delete(0, tk.END)
        download_entry.insert(0, filename)
    else:
        print("No file selected for upload.")

def download_file(filename):
    client_socket.send('download'.encode())
    client_socket.send(filename.encode())
    file_data = client_socket.recv(1024)
    with open(filename, 'wb') as f:
        f.write(file_data)

def send_message():
    message = message_entry.get()
    recipient = recipient_entry.get()
    if recipient:
        client_socket.send(f"{recipient},{message}".encode())
    else:
        client_socket.send(message.encode())
    message_entry.delete(0, tk.END)
    recipient_entry.delete(0, tk.END)

def block_user():
    blocked_username = recipient_entry.get()
    if blocked_username:
        client_socket.send(f"block,{blocked_username}".encode())
        recipient_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            chat_box.insert(tk.END, message + '\n')
        except ConnectionResetError:
            print("Connection lost. Please check the server.")
            break

client_id = str(uuid.uuid4())[:5]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
username = input("Enter your username: ")
password = input("Enter your password: ")

client_socket.send(f"{username},{password}".encode())
client_socket.send((username + " joined the session 😃").encode()) 

root = tk.Tk()
root.title("Chat Room for " + username)
root.configure(bg="#282424")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 9), padding=3, relief="raised")
style.configure("TLabel", font=("Segoe UI", 9), padding=3, relief="raised")
style.configure("TEntry", font=("Segoe UI", 9), relief="raised")

chat_box = scrolledtext.ScrolledText(root, width=30, height=17, bg="#FFFFFF", fg="#000000", font=("Segoe UI", 10), padx=8, pady=8)
chat_box.pack(padx=8, pady=8)

ttk.Label(root, text="Enter message below:", background="#ECE5DD").pack(padx=10, pady=5)
message_entry = ttk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5)

ttk.Label(root, text="Enter recipient username (Leave blank for broadcast):", background="#ECE5DD").pack(padx=10, pady=5)
recipient_entry = ttk.Entry(root, width=40)
recipient_entry.pack(padx=10, pady=5)

send_button = ttk.Button(root, text="Send", command=send_message, style="TButton")
send_button.pack(padx=10, pady=5)

block_button = ttk.Button(root, text="Block", command=block_user, style="TButton")
block_button.pack(padx=8, pady=6)

ttk.Label(root, text="Upload file:", background="#ECE5DD").pack(padx=10, pady=5)
upload_entry = ttk.Entry(root, width=40)
upload_entry.pack(padx=10, pady=5)

select_button = ttk.Button(root, text="Select File", command=select_file, style="TButton")
select_button.pack(padx=10, pady=5)
 
upload_button = ttk.Button(root, text="Upload", command=lambda: upload_file(upload_entry.get()), style="TButton")
upload_button.pack(padx=10, pady=5)

ttk.Label(root, text="Download file:", background="#ECE5DD").pack(padx=10, pady=5)
download_entry = ttk.Entry(root, width=40)
download_entry.pack(padx=10, pady=5)
download_button = ttk.Button(root, text="Download", command=lambda: threading.Thread(target=download_file, args=(download_entry.get(),)).start(), style="TButton")
download_button.pack(padx=10, pady=4)

exit_button = ttk.Button(root, text="Exit", command=lambda: [client_socket.send((username + " left the chat 😢").encode()), root.quit()], style="TButton")
exit_button.pack(padx=10, pady=4)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()
