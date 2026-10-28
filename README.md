Hello! This is a simple, low-security chat room that utilizes a key. 
You can generate this key using the `cryptography.fernet` library.
Please note that the key must be identical across all clients.
Furthermore, messages remain unreadable to the server itself.
You will also need the server's IP address; the device acting as the server must share its IP
address with the clients. I hope you enjoy it!
Also, make sure that your Windows Firewall allows access to the specified port!!!