from socket import *
from DHCP.Util.log import *

serverName = 'DHCP-Server'
serverPort = 67
tcpSocket = socket(AF_INET, SOCK_STREAM)


def tcp_client(message):
    tcpSocket.connect((serverName, serverPort))
    tcpSocket.send(message.encode())
    address, response = tcpSocket.recv(1024)
    tcp_client_tuple = (address, response)
    tcpSocket.close()
    return tcp_client_tuple


def tcp_server():
    tcpSocket.bind(('', serverPort))
    tcpSocket.listen(1)
    print('DHCP Server is Listening (TCP)')
    server_log_stat("DHCP Server is Listening (TCP)")

    while True:
        connection_socket, address = tcpSocket.accept()
        request = connection_socket.recv(1024).decode()
        tcp_server_tuple = (connection_socket, address, request)
        connection_socket.close()
        return tcp_server_tuple


