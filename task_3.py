import machine  # Import the machine package
import network  # Import the network package
import socket  # Import the socket package
import json  # Import the json package

# Create a WLAN access point
ap = network.WLAN(network.AP_IF)
ap.active(True)  # Activate access point
ap.config(essid='ESP32-JRS')  # The name of the access point
ap.config(authmode=3, password='jjjrrrsss')  # Password needed to connect

# Defining the input pins used
button1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
sensor = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
pins = [machine.Pin(i, machine.Pin.IN) for i in (12, 13)]

# Define a few variables that hold the device and register address values
address = 24
temp_reg = 5
res_reg = 8
data = bytearray(2)


# Sensor reading data transformed to degrees celsius
def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp


# Creates HTML-based web pages
html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> 
        %s
    </body>
</html>
"""

# Get tuple address format for socket module
# 0.0.0.0 means "all IPv4 addresses on the local machine", 80 is the port number
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()  # Creating a socket object
s.bind(addr)  # Bind the socket to above IP and port number
s.listen(1)  # The maximum number of queued connections, before the server starts to accept connection request from client

print('listening on', addr)  # Print server address

while True:
    # The server accepts a connection
    cl, addr = s.accept()  # "cl" is a new socket object usable to send and receive data on the connection
                           # addr is the (IP, port) bound to the client
    print('client connected from', addr)  # Print client address
    cl_file = cl.makefile('rwb', 0)  # Create a file associated with the socket "cl", which recieves the requests from the client
    get_request = cl_file.readline().decode('ascii')  # The first line is b'Get /path HTTP/1.1\r\n', and convert it to normal python string
    print(get_request)
    try:
        path = get_request.split()[1]  # split 'get_request' by whitespace, and get the resource path
    except:
        break
    # Make every path end in '/'
    if path[-1] != '/':
        path = path + '/'
    # read the other information in the request
    while True:
        line = cl_file.readline()  # Read the requests from the client
        print(line)
        if not line or line == b'\r\n':
            break

    sensor.readfrom_mem_into(address, temp_reg, data)
    # ***A simple request–response message system: {resources path: resources content}
    api = {"/pins/": json.dumps(["pin12", "pin13"]),
           "/pins/pin12/": json.dumps(machine.Pin(12, machine.Pin.IN).value()),
           "/pins/pin13/": json.dumps(machine.Pin(13, machine.Pin.IN).value()),
           "/sensors/": json.dumps(["temperature_sensor"]),
           "/sensors/temperature_sensor/": json.dumps(temp_c(data))}

    # If no path specified, return full information
    if path == '/':
        response = html % json.dumps(api)
    # match request with response based on api map
    else:
        try:
            response = html % api[path]
        except:
            response = html % "404 NOT FOUND"  # If no such path, return "404 NOT FOUND"

    cl.send(response)  # Send 'html' on the socket 'cl'
    cl.close()  # Close the connection




