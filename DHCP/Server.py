from DHCP.Transport.TCP import *
from DHCP.Util.ipPool import *
from DHCP.Util.log import *
from DHCP.Util.msgDecoder import *

"""Initial State & Variable Declaration"""
serverName = 'DHCP-Server'
serverPort = 67
udp_socket = socket(AF_INET, SOCK_DGRAM)
ip.version = 4
udp_socket.bind(('', serverPort))
server_log_stat("DHCP Server is Listening (UDP)")
dhcp_ip = IPAddress('192.168.1.2')
sid = str(dhcp_ip)
dns_ip = IPAddress('172.20.1.10')
dgw_ip = IPAddress('192.168.1.1')
netmask = IPAddress('255.255.255.0')
client_default_addr = IPAddress('0.0.0.0')
nack_message_yiaddr = IPAddress('0.0.0.0')
nack_message_dgw = IPAddress('0.0.0.0')
nack_message_dns = IPAddress('0.0.0.0')
nack_message_mask = IPAddress('0.0.0.0')
ip_pool = IPPool()
assigned_dict = {'IP Address': None, 'Host Name': None, 'MAC Address': None}

server_log_ip(dns_ip, dgw_ip, netmask, IPAddress(ip_pool.get_first()), IPAddress(ip_pool.get_last()))
server_log_assigned_ip_addr("Assigned IP Addresses List: ")
server_log_assigned_ip_divider()

"""Waiting For Client Discovey Message"""
server_log_stat("Waiting for Client Discovery")
while True:
    req, addr = udp_socket.recvfrom(2048)
    msg = req.decode('utf-8')
    udp_server_tuple = (addr, msg)
    client_address = udp_server_tuple[0]
    client_msg = udp_server_tuple[1]
    client_request = msg_decoder(client_msg)
    client_chaddr = client_request.chaddr
    client_xid = client_request.xid
    ip_offer = ip_pool.assign_ip()
    ip_availability = True
    if ip_offer == (IPAddress('0.0.0.0')):
        ip_availability = False
    if(OperationCode.operation1.value == client_request.op):
        if (MessageType.type1.value == client_request.option.msg_type):
            offer_msg = MessageFormat(OperationCode.operation2.value, client_default_addr,
                                      ip_offer, client_chaddr, MessageType.type2.value)
            server_log_stat("DHCP Discovery Message Received")
            offer_msg.xid = client_xid
            offer_msg.option.mask = netmask
            offer_msg.option.renewtime = 0
            offer_msg.option.rebindtime = 0
            offer_msg.option.leasetime = 0
            offer_msg.option.sid = str(dhcp_ip)
            offer_msg.option.router = dgw_ip
            offer_msg.option.dns = dns_ip
            msg = offer_msg.__str__()
            server_log_stat("Sending Offer Message")
            udp_socket.sendto(msg.encode(), client_address)
            server_log_stat("DHCP Request Message Received")
        elif(MessageType.type3.value == client_request.option.msg_type):
            if ip_availability:
                ack_msg = MessageFormat(OperationCode.operation2.value, client_default_addr,
                                        ip_offer, client_chaddr, MessageType.type4.value)
                ack_msg.xid = client_xid
                ack_msg.option.mask = netmask
                ack_msg.option.renewtime = 0
                ack_msg.option.rebindtime = 0
                ack_msg.option.leasetime = 0
                ack_msg.option.sid = sid
                ack_msg.option.router = dgw_ip
                ack_msg.option.dns = dns_ip
                msg = ack_msg.__str__()
                server_log_stat("Sending ACK Message")
                udp_socket.sendto(msg.encode(), client_address)
                server_log_stat("ACK Message Sent")
                server_log_divider()
                assigned_dict['IP Address'] = ack_msg.yiaddr
                assigned_dict['Host Name'] = client_request.option.hname
                assigned_dict['MAC Address'] = client_request.chaddr
                server_log_assigned_ip_addr("IP Address: " + str(assigned_dict['IP Address']))
                server_log_assigned_ip_addr("MAC Address:" + str(assigned_dict['MAC Address']))
                server_log_assigned_ip_addr("Host Name: " + str(assigned_dict['Host Name']))
                server_log_assigned_ip_divider()
            else:
                nack_msg = MessageFormat(OperationCode.operation2.value, client_default_addr,
                                         nack_message_yiaddr, client_chaddr, MessageType.type5.value)
                nack_msg.xid = client_xid
                nack_msg.option.sid = sid
                nack_msg.option.mask = nack_message_mask
                nack_msg.option.router = nack_message_dgw
                nack_msg.option.dns = nack_message_dns
                msg = nack_msg.__str__()
                server_log_stat("Sending NACK Message")
                udp_socket.sendto(msg.encode(), client_address)
                server_log_stat("NACK Message Sent")
                server_log_divider()

