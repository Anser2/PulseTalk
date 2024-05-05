import tkinter as tk
from tkinter import scrolledtext
import socket
import threading 
import uuid  # Import the uuid module for generating unique IDs
from tkinter import filedialog

def select_file():
    filename = filedialog.askopenfilename()
    upload_entry.delete(0, tk.END)  # Clear the entry field
    upload_entry.insert(0, filename)  # Insert the selected filename
    
    # Send the filename and file data to the server
    client_socket.send(filename.encode())


def upload_file(filename):
    # Check if the filename is not empty
    if filename:
        # Send the 'upload' command to the server
        client_socket.send('upload'.encode())
        
        # Read the file data
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        # Send the filename and file data to the server
        client_socket.send(filename.encode())
        client_socket.send(file_data)

        # Set the download_entry field to the filename of the uploaded file
        download_entry.delete(0, tk.END)  # Clear the entry field
        download_entry.insert(0, filename)  # Insert the filename
    else:
        print("No file selected for upload.")

def download_file(filename):
    # Send the filename to the server
    client_socket.send(filename.encode())
    
    # Receive the file data from the server
    file_data = client_socket.recv(1024)
    
    # Save the file locally
    with open(filename, 'wb') as f:
        f.write(file_data)

def send_message():
    message = message_entry.get()
    client_socket.send(("--> "+ username+": " +message ).encode())
    message_entry.delete(0, tk.END)


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            
            chat_box.insert(tk.END, message + '\n')
        except Exception as e:
            print(f"Error: {str(e)}")
            client_socket.send(("--> "+ username+": " + "An error occurred" ).encode())
            client_socket.close()
            break
            client_socket.send(("--> "+ username+": " +message ).encode())
            message_entry.delete(0, tk.END)

# Generate a unique ID for the client
client_id = str(uuid.uuid4())[:5]  # Generate a unique IDaa with only the first 8 characters

# Set up client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
username = input("Enter your username: ")
password = input("Enter your password: ")

# Send the username and password to the server
client_socket.send(f"{username},{password}".encode())
# Send the client ID to the server
client_socket.send((username + " joined the session ^_^").encode()) 

# Create GUI
root = tk.Tk()
root.title("Chat Room for "+ username)

chat_box = scrolledtext.ScrolledText(root, width=50, height=20)
chat_box.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)
# New entry field for the filename to upload
upload_entry = tk.Entry(root, width=40)
upload_entry.pack(padx=10, pady=5)

select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(padx=10, pady=5)

upload_button = tk.Button(root, text="Upload", command=lambda: upload_file(upload_entry.get()))
upload_button.pack(padx=10, pady=5)

# New entry field for the filename to download
download_entry = tk.Entry(root, width=40)
download_entry.pack(padx=10, pady=5)
download_button = tk.Button(root, text="Download", command=lambda: threading.Thread(target=download_file, args=(download_entry.get(),)).start())
download_button.pack(padx=10, pady=5)
# New button for downloading files
#download_button = tk.Button(root, text="Download", command=lambda: download_file(download_entry.get()))
#download_button.pack(padx=10, pady=5)

exit_button = tk.Button(root, text="Exit", command=lambda: [client_socket.send((client_id + " left the chat :(").encode()), root.quit()])
exit_button.pack(padx=10, pady=5)




# Start thread for receiving messages 
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


root.mainloop() 

