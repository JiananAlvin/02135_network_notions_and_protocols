import machine # import the machine package
import network # imports the network package
import socket # imports the socket package

# Create a WLAN access point
ap = network.WLAN (network.AP_IF)
ap.active (True) # while true, its on
ap.config (essid = 'ESP32-JRS') # the name of the accesspoint
ap.config (authmode = 3, password = 'WiFi-password') # password needed to connect

# Defining the input pins used
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)] 

# Creates a HTML-based web server, that reports the status of the pins  
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

# defining the address, to the host IP-adress as well as the port number.
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket() # Creating a socket object
s.bind(addr) # assign IP and port number to create a server. 
s.listen(1) # limits unaccepted requests the server can take at a time to 1.

print('listening on', addr) # Printing the current address we are connecting to.

while True:
    cl, addr = s.accept() # Getting information about the client socket and address, accept connection request
    print('client connected from', addr) # Print client address
    cl_file = cl.makefile('rwb', 0) # Create a file associated with the client socket
    while True:
        line = cl_file.readline()
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
