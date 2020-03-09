from socket import *
from DHCP.Util.log import *

serverName = 'DHCP-Server'
serverPort = 67
udp_socket = socket(AF_INET, SOCK_DGRAM)


def udp_client(message, ip):
    if ip == "BROADCAST":
        udp_socket.bind(('', 0))
        udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        udp_socket.sendto(message.encode(), ('<broadcast>', serverPort))
    else:
        udp_socket.sendto(message.encode(), (ip, serverPort))
    response, address = udp_socket.recvfrom(2048)
    udp_client_tuple = (address, response)
    udp_socket.close()
    return udp_client_tuple


def udp_server():
    udp_socket.bind(('', serverPort))
    while True:
        request, address = udp_socket.recvfrom(2048)
        msg = request.decode()
        udp_server_tuple = (address, msg)
        return udp_server_tuple
