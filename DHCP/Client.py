from tkinter import *
from DHCP.Transport.TCP import *
from DHCP.Util.log import *
from DHCP.Util.msgDecoder import *

serverPort = 67
udp_socket = socket(AF_INET, SOCK_DGRAM)
ip.version = 4

udp_socket.bind(('', 0))
udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


def get_mac_address():
    mac_addr = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    return mac_addr


"""Initial State & Variable Declaration"""
client_log_stat("Initial State")
init_ip_addr = IPAddress('0.0.0.0')
init_dgw = IPAddress('0.0.0.0')
init_dns = IPAddress('0.0.0.0')
init_mask = IPAddress('0.0.0.0')
mac_address = get_mac_address()
hostname = gethostname()
client_log_ip(init_ip_addr, init_mask, init_dgw, init_dns)

"""DHCP Server Discovery State"""
client_log_stat("DHCP Discovery")
discover_msg = MessageFormat(OperationCode.operation1.value, init_ip_addr, IPAddress('0.0.0.0'),
                             mac_address, MessageType.type1.value)
discover_msg.option.cid = str(mac_address)
discover_msg.option.hname = hostname
msg = discover_msg.__str__()
client_log("DHCP Discovery Message: " + msg)
client_log_divider()
client_log("Operation Code: " + str(discover_msg.op))
client_log("Hardware Type: " + str(discover_msg.htype))
client_log("Oeration Address Length: " + str(discover_msg.hlen))
client_log("Hops: " + str(discover_msg.hops))
client_log("Transaction ID: " + str(discover_msg.xid))
client_log("Seconds: " + str(discover_msg.secs))
client_log("Flags: " + str(discover_msg.flags))
client_log("Client IP Address (ciaddr): " + str(discover_msg.ciaddr))
client_log("Your IP Address (yiaddr): " + str(discover_msg.yiaddr))
client_log("Server IP Address (siaddr): " + str(discover_msg.siaddr))
client_log("Relay IP Address (giaddr): " + str(discover_msg.giaddr))
client_log("Client Ethernet Address (chaddr): " + str(discover_msg.chaddr))
client_log("Server Host Name: " + discover_msg.sname)
client_log("Server File Name: " + discover_msg.file)
client_log("OPTION FIELDS: ")
client_log("    DHCP Message Type: " + discover_msg.option.msg_type)
client_log("    Client Identifier: " + discover_msg.option.cid)
client_log("    Host Name: " + discover_msg.option.hname)
client_log("    Parameter Request List: " + str(discover_msg.option.parreqlist))
client_log_divider()

udp_socket.sendto(msg.encode('utf-8').strip(), ('<broadcast>', serverPort))
"""Wait For DHCP Server Offer..."""
client_log_stat("Wait For DHCP Server Offer")
resp, addr = udp_socket.recvfrom(2048)
msg = resp.decode()
udp_client_tuple = (addr, msg)
client_log_stat("Server Offer Received")
server_address = udp_client_tuple[0]
server_offer = udp_client_tuple[1]
client_log("   From: " + str(server_address))
client_log("   Offer Message: " + str(server_offer))
server_reply = msg_decoder(server_offer)
client_log_divider()
client_log("Operation Code: " + str(server_reply.op))
client_log("Hardware Type: " + str(server_reply.htype))
client_log("Oeration Address Length: " + str(server_reply.hlen))
client_log("Hops: " + str(server_reply.hops))
client_log("Transaction ID: " + str(server_reply.xid))
client_log("Seconds: " + str(server_reply.secs))
client_log("Flags: " + str(server_reply.flags))
client_log("Client IP Address (ciaddr): " + str(server_reply.ciaddr))
client_log("Your IP Address (yiaddr): " + str(server_reply.yiaddr))
client_log("Server IP Address (siaddr): " + str(server_reply.siaddr))
client_log("Relay IP Address (giaddr): " + str(server_reply.giaddr))
client_log("Client Ethernet Address (chaddr): " + str(server_reply.chaddr))
client_log("Server Host Name: " + server_reply.sname)
client_log("Server File Name: " + server_reply.file)
client_log("OPTION FIELDS: ")
client_log("    DHCP Message Type: " + server_reply.option.msg_type)
client_log("    Subnet Mask: " + str(server_reply.option.mask))
client_log("    Renewal Time: " + str(server_reply.option.renewtime))
client_log("    Rebinding Time: " + str(server_reply.option.rebindtime))
client_log("    Lease Time: " + str(server_reply.option.leasetime))
client_log("    Server Identifier: " + str(server_reply.option.sid))
client_log("    Router: " + str(server_reply.option.router))
client_log("    DNS Server: " + str(server_reply.option.dns))
client_log_divider()


"""Sending DHCP Request Message"""
client_log_stat("DHCP Request")
if(OperationCode.operation2.value == server_reply.op):
    if(MessageType.type2.value == server_reply.option.msg_type):
        request_msg = MessageFormat(OperationCode.operation1.value, init_ip_addr,
                                    IPAddress('0.0.0.0'), mac_address, MessageType.type3.value)
        request_msg.option.cid = str(mac_address)
        request_msg.option.req_addr = server_reply.yiaddr
        request_msg.option.sid = server_reply.option.sid
        request_msg.option.hname = hostname
        msg = request_msg.__str__()
        client_log("DHCP Request Message: " + msg)
        client_log_divider()
        client_log("Operation Code: " + str(request_msg.op))
        client_log("Hardware Type: " + str(request_msg.htype))
        client_log("Oeration Address Length: " + str(request_msg.hlen))
        client_log("Hops: " + str(request_msg.hops))
        client_log("Transaction ID: " + str(request_msg.xid))
        client_log("Seconds: " + str(request_msg.secs))
        client_log("Flags: " + str(request_msg.flags))
        client_log("Client IP Address (ciaddr): " + str(request_msg.ciaddr))
        client_log("Your IP Address (yiaddr): " + str(request_msg.yiaddr))
        client_log("Server IP Address (siaddr): " + str(request_msg.siaddr))
        client_log("Relay IP Address (giaddr): " + str(request_msg.giaddr))
        client_log("Client Ethernet Address (chaddr): " + str(request_msg.chaddr))
        client_log("Server Host Name: " + request_msg.sname)
        client_log("Server File Name: " + request_msg.file)
        client_log("OPTION FIELDS: ")
        client_log("    DHCP Message Type: " + request_msg.option.msg_type)
        client_log("    Client Identifier: " + request_msg.option.cid)
        client_log("    Requested Address: " + str(request_msg.option.req_addr))
        client_log("    Server Identifier: " + request_msg.option.sid)
        client_log("    Host Name: " + request_msg.option.hname)
        client_log("    Parameter Request List: " + str(request_msg.option.parreqlist))
        client_log_divider()
        udp_socket.sendto(msg.encode('utf-8').strip(), ('<broadcast>', serverPort))
        """Wait For DHCP Server Acknowledge..."""
        client_log_stat("Wait For DHCP Server Acknowledge")
        resp, addr = udp_socket.recvfrom(2048)
        msg = resp.decode()
        udp_client_tuple = (addr, msg)
        client_log_stat("Server ACK Received")
        server_address = udp_client_tuple[0]
        server_ack = udp_client_tuple[1]
        client_log("    From: " + str(server_address))
        client_log("    ACK Message: " + str(server_ack))
        ack_server_reply = msg_decoder(server_ack)
        client_log_divider()
        client_log("Operation Code: " + str(ack_server_reply.op))
        client_log("Hardware Type: " + str(ack_server_reply.htype))
        client_log("Oeration Address Length: " + str(ack_server_reply.hlen))
        client_log("Hops: " + str(ack_server_reply.hops))
        client_log("Transaction ID: " + str(ack_server_reply.xid))
        client_log("Seconds: " + str(ack_server_reply.secs))
        client_log("Flags: " + str(ack_server_reply.flags))
        client_log("Client IP Address (ciaddr): " + str(ack_server_reply.ciaddr))
        client_log("Your IP Address (yiaddr): " + str(ack_server_reply.yiaddr))
        client_log("Server IP Address (siaddr): " + str(ack_server_reply.siaddr))
        client_log("Relay IP Address (giaddr): " + str(ack_server_reply.giaddr))
        client_log("Client Ethernet Address (chaddr): " + str(ack_server_reply.chaddr))
        client_log("Server Host Name: " + ack_server_reply.sname)
        client_log("Server File Name: " + ack_server_reply.file)
        client_log("OPTION FIELDS: ")
        client_log("    DHCP Message Type: " + ack_server_reply.option.msg_type)
        client_log("    Subnet Mask: " + str(ack_server_reply.option.mask))
        client_log("    Renewal Time: " + str(ack_server_reply.option.renewtime))
        client_log("    Rebinding Time: " + str(ack_server_reply.option.rebindtime))
        client_log("    Lease Time: " + str(ack_server_reply.option.leasetime))
        client_log("    Server Identifier: " + str(ack_server_reply.option.sid))
        client_log("    Router: " + str(ack_server_reply.option.router))
        client_log("    DNS Server: " + str(ack_server_reply.option.dns))
        client_log_divider()


client_log_stat("Final State (IP Acquired From DHCP Server)")
if ack_server_reply.yiaddr == init_ip_addr:
    client_log_stat("   NACK Received From DHCP Server")
ip_addr = ack_server_reply.yiaddr
dgw = ack_server_reply.option.router
dns = ack_server_reply.option.dns
mask = ack_server_reply.option.mask
client_log_ip(ip_addr, mask, dgw, dns)
client_log_divider()
client_log_divider()


"""
# TODO: Change value of IP addresses and print GUI
def client_exit():
    exit()


def open_log():
    startfile('client_Log.txt')


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("DHCP Client")
        self.pack(fill=BOTH, expand=1)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Open Log File", command=open_log)
        file.add_command(label="Exit", command=client_exit)
        menu.add_cascade(label="File", menu=file)
        edit = Menu(menu)
        Label(self, text="Initialize State IP Addresses:").pack()
        ip_text = ['IP Address : ', init_ip_addr]
        Label(self, text="{} {}".format(ip_text[0], ip_text[1])).pack()
        subnet_text = ['Subnet Mask: ', init_mask]
        Label(self, text="{} {}".format(subnet_text[0], subnet_text[1])).pack()
        default_gateway_text = ['Default Gateway: ', init_dgw]
        Label(self, text="{} {}".format(default_gateway_text[0], default_gateway_text[1])).pack()
        dns_text = ['Preferred DNS Server: ', init_dns]
        Label(self, text="{} {}".format(dns_text[0], dns_text[1])).pack()
        Label(self, text="************************************************").pack()


root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()
"""
