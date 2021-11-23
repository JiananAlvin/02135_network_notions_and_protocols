import machine  # Import the machine package
import network  # Import the network package
import socket  # Import the socket package

# Create a WLAN access point
ap = network.WLAN(network.AP_IF)
ap.active(True)  # Activate access point
ap.config(essid='ESP32-JRS')  # The name of the access point
ap.config(authmode=3, password='WiFi-password')  # Password needed to connect

# Defining the input pins used
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

# Creates a HTML-based web page, that reports the status of the pins
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

# Get tuple address format for socket module
# 0.0.0.0 means "all IPv4 addresses on the local machine", 80 is the port number
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()  # Creating a socket object
s.bind(addr)  # Bind the socket to above IP and port number
s.listen(1)  # The maximum number of queued connections, before the server starts to accept connection request from client

print('listening on', addr)   # Print server address

while True:
    # The server accepts a connection
    cl, addr = s.accept()  # "cl" is a new socket object usable to send and receive data on the connection
                           # addr is the (IP, port) bound to the client
    print('client connected from', addr)  # Print client address
    cl_file = cl.makefile('rwb', 0)  # Create a file associated with the socket "cl", which recieves the requests from the client
    while True:
        line = cl_file.readline()  # Read the requests from the client
        # print(line)
        if not line or line == b'\r\n':
            break
    # Each row in [Pin|Value]
    # 'rows' is a list containing each element '<tr><td>Pin</td><td>Pin_Value</td></tr>'
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)  # join each element in 'rows' with the new line character '\n',
                                       # and then pass the joint string to 'html'
    cl.send(response)  # Send 'html' on the socket 'cl'
    cl.close()  # Close the connection
