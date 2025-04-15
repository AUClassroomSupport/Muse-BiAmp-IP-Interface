from mojo import context
import socket
import asyncio

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.184.42.54', 23))
def handleData(data):
    context.log.info(str(data))
    wontCommands = []
    dontCommands = []
    i = 0

    while i < len(data):
        if data[i:i+2] == bytes([255,253]):
            wontCommands.append(data[i+2])
        elif data[i:i+2] == bytes([255,251]):
            dontCommands.append(data[i+2])
        i += 3

    context.log.info("Wont Command Count: " + str(len(wontCommands)))
    context.log.info("Dont Command Count: " + str(len(dontCommands)))

    for byte in wontCommands:
        response = bytes([255, 252, byte])
        clientsocket.send(response)
    wontCommands.clear()

    for byte in dontCommands:
        response = bytes([255, 254, byte])
        clientsocket.send(response)
    
    wontCommands.clear()
    dontCommands.clear()
handleData(clientsocket.recv(2048))
handleData(clientsocket.recv(2048))
handleData(clientsocket.recv(2048))
data = clientsocket.recv(2048)
context.log.info(str(data))
clientsocket.send("admin".encode('ascii') + bytes([10]))
handleData(clientsocket.recv(2048))
handleData(clientsocket.recv(2048))
data = clientsocket.recv(2048)
context.log.info(str(data))
clientsocket.send("#E!ki986".encode('ascii') + bytes([10]))
data = clientsocket.recv(2048)
context.log.info(str(data))
data = clientsocket.recv(2048)
context.log.info(str(data))

clientsocket.send("2108WlsLvl set level 1 -60".encode('ascii') + bytes([10]))
data = clientsocket.recv(2048)
context.log.info(str(data))

clientsocket.send("2108WlsLvl set level 1 0".encode('ascii') + bytes([10]))
data = clientsocket.recv(2048)
context.log.info(str(data))

clientsocket.send("2108WlsLvl set level 1 -60".encode('ascii') + bytes([10]))
data = clientsocket.recv(2048)
context.log.info(str(data))
clientsocket.send("2108WlsLvl set level 1 -40".encode('ascii') + bytes([10]))
data = clientsocket.recv(2048)
context.log.info(str(data))

# leave this as the last line in the Python script
context.run(globals())
