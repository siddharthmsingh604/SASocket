import socket

class EchoClient:

    def __init__(self,server_addr,server_port,header = 64,footer="~",format = "utf-8"):
        self.server_addr = server_addr
        self.server_port = server_port
        self.header = header
        self.footer = footer
        self.format = format

    def __enter__(self):
        self.client_scoket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_scoket.connect((self.server_addr,self.server_port))
        return(self)

    def handleMessage(self,message):
        message = message.encode(self.format)
        message_length = str(len(message))
        message_length += " " * (self.header-len(message_length))
        message_length = message_length.encode(self.format)
        return([message_length,message])

    def sendMessage(self,message):
        header_message = self.handleMessage(message)
        self.client_scoket.send(header_message[0])
        self.client_scoket.send(header_message[1])
        return(self)

    def __exit__(self,exc_type,exc_value,traceback):
        print(f"[TERMINATING CLIENT]")
        self.client_scoket.close()

with EchoClient("192.168.1.26",65432) as client:
    connected = True
    while(connected):
        message = input("Message: ")
        if(message == client.footer):
            client.sendMessage(message)
            connected = False
        else:
            client.sendMessage(message)