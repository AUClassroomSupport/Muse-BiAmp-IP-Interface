from mojo import context
import asyncio
transport = None
class BiampTelnetClientProtocol(asyncio.Protocol):

    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost
        self.transport = None
        self.loggedIn = False
    
    def connection_made(self, transport):
        self.transport = transport
        transport = transport
        context.log.info("Connection Established!")
    
    def data_received(self, data):
        # Per Biamp Telnet Session Negotiation, if first byte is 0xFF (255) its a Interpret as Command
        # Must respond to any command as listed in link below
        # https://support.biamp.com/Tesira/Control/Telnet_session_negotiation_in_Tesira
        if data[0] == 255:
            context.log.info("COMMAND RECEIVED")
            wontCommands = []
            dontCommands = []
            i = 0
            
            # Commands come as 3 bytes starting with 255 and then will be a 253 or 251
            while i < len(data):
                if data[i:i+2] == bytes([255,253]):
                    wontCommands.append(data[i+2])
                elif data[i:i+2] == bytes([255,251]):
                    dontCommands.append(data[i+2])
                i += 3

            # respond to any IAC messages
            for byte in wontCommands:
                response = bytes([255, 252, byte])
                self.transport.write(response)
            wontCommands.clear()

            for byte in dontCommands:
                response = bytes([255, 254, byte])
                self.transport.write(response)
            dontCommands.clear()
        
        # If we see login or password, attempt to log in
        elif "login" in str(data):
            context.log.info("Saw login Prompt")
            self.transport.write("admin".encode('ascii') + bytes([10]))

        elif "Password" in str(data):
            context.log.info("Saw password Prompt")
            self.transport.write("#E!ki986".encode('ascii') + bytes([10]))
        elif "Welcome" in str(data):
            context.log.info ("Login Successful")
            self.loggedIn = True
        else:
            context.log.info(str(data))

    
    def connection_lost(self, exc):
        context.log.info('The server closed the connection')
        self.on_con_lost.set_result(True)

async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_connection(lambda: BiampTelnetClientProtocol(on_con_lost),'10.184.42.54', 23)

    try:
        await on_con_lost
    finally:
        transport.close()

def call(path, args):
    contxt.log.info(path)
    context.log.info(args)

asyncio.run(main())

#clientsocket.send("2108WlsLvl set level 1 -40".encode('ascii') + bytes([10]))

# leave this as the last line in the Python script
context.run(globals())
