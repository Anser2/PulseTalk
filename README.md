# Overview
This project is a Chat Room application implemented using Python. The application allows users to connect to a central server, send messages to other users or broadcast messages to all connected users, upload and download files, and block specific users. It features a graphical user interface (GUI) built with Tkinter, and uses sockets for network communication. The server manages user authentication, file storage, and maintains a list of blocked users.

![image](https://github.com/Anser2/PulseTalk/assets/130187355/95e38050-1ab7-4c23-b6b0-13e61fdf992a)


# Features
User Authentication: Users can register or log in with a username and password. The server stores user credentials in a SQLite database.
Messaging: Users can send direct messages to other users or broadcast messages to all users in the chat room.
File Transfer: Users can upload files to the server and download files from the server.
User Blocking: Users can block specific users to prevent them from sending messages.
GUI: The application includes a user-friendly graphical interface built with Tkinter.

# Requirements
Python 3.x,
Tkinter,
SQLite3

# Installation
Clone the repository:
git clone https://github.com/yourusername/PulseTalk.git ,
cd PulseTalk

Ensure you have Python 3 installed. You can download it from python.org.
Install the required Python packages:
pip install tkinter

# Usage
Server
Run the server:
python server.py
The server will start and listen on port 5555.

Client
Run the client:
python client.py
Enter your username and password when prompted. If it is a new username, an account will be created for you.

Blocking a User
Enter the username of the user you want to block in the recipient entry field.
Click the "Block" button. This will prevent the blocked user from sending messages to you.
File Transfer
Upload a File:
Select a file using the "Select File" button.
Click the "Upload" button to upload the selected file to the server.
Download a File:
Enter the filename in the download entry field.
Click the "Download" button to download the specified file from the server.
Code Structure
client.py: Handles the client-side operations including the GUI, sending and receiving messages, file uploads and downloads, and user blocking.
server.py: Manages server-side operations including user authentication, handling client connections, processing messages, and file transfers.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Feel free to modify this description to better match your project specifics or to add any additional information you find relevant.
