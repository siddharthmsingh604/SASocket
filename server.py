import socket
import threading

class EchoServer:

    def __init__(self,addr,port,timeout=8,header=64,format = "utf-8",footer = "~"):
        self.addr = addr
        self.port = port
        self.server_socket = None
        self.timeout = timeout
        self.header = header
        self.format = format
        self.footer = footer

    def __enter__(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((self.addr,self.port))
        self.server_socket.listen()
        print(f"[LISTENING] at port: {self.port} and address: {self.addr}")
        return self
    
    def start(self):
        while(True):
            server_client_socket , client_address = self.server_socket.accept()
            print(f"[CONNECTED] Client details are: address: {client_address[0]} port: {client_address[1]}")
            client_thread = threading.Thread(target = self.handle_client, args = (server_client_socket,client_address))
            client_thread.start()
            print(f"[THREADED] Total Active Connections: {threading.active_count()-1}")
    
    def handle_client(self,server_client_socket,client_address):
        connection_status = True
        with server_client_socket:
            while(connection_status):
                msg_length = server_client_socket.recv(self.header).decode(self.format)
                message = server_client_socket.recv(int(msg_length)).decode(self.format)
                if (message == self.footer):
                    connection_status = False
                    print(f"[DISCONNECTED] Client with IP: {client_address[0]}")
                else:
                    print(f"[MESSAGE] from IP:{client_address[0]} at PORT:{client_address[1]} {message}")


    def __exit__(self, exc_type, exc_value, traceback):
        print("[TERMINATING SERVER]")
        #print(f"{exc_type} {exc_value} {traceback}")
        self.server_socket.close()
    
with EchoServer("192.168.1.26",65432) as server:
    server.start()