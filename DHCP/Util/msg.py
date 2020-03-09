import uuid
from DHCP.Util.enums import *
from netaddr import *


def xid_generator():
    id = uuid.uuid1()
    id = id.int
    return id


class MessageOptionFields:
    msg_type = None  # Four message types (1 = DHCPDISCOVER, 2 = DHCPOFFER, 3 = DHCPREQUEST and 4 = DHCPACK)
    mask = None  # Subnet Mask
    cid = None  # Client Identifier (Equal to Client MAC Address)
    req_addr = None  # Client Requested Address (for Request Message)
    hname = None  # Client Hostname
    parreqlist = None  # Parameter Requested List (filled by Client to Identify Requested Parameters)
    sid = None  # Server Identifier (Equal to Server IP Address)
    router = None  # Router or Default Gateway
    dns = None  # Domain Name Server IP Address
    renewtime = None  # Renewal Time Value
    rebindtime = None  # Rebinding Time Value
    leasetime = None  # IP Address Lease Time

    def __init__(self, msg_type):
        self.msg_type = msg_type
        self.mask = IPAddress('0.0.0.0')
        self.cid = 0
        self.req_addr = IPAddress('0.0.0.0')
        self.hname = "NoName"
        self.parreqlist = 0
        self.sid = 0
        self.router = IPAddress('0.0.0.0')
        self.dns = IPAddress('0.0.0.0')
        self.renewtime = 0
        self.rebindtime = 0
        self.leasetime = 0


class MessageFormat:
    """Default DHCP Message Format Fields"""
    op = None  # Operation Code (1 = Client Request, 2 = Server Reply)
    htype = None  # Hardware Type (example: Ethernet = 1)
    hlen = None  # Hardware Address Length (MAC Address is 6 bytes)
    hops = None  # Number of relay agents that have forwarded this message
    xid = None  # Transaction Identifier (Used by clients to match responses from servers)
    secs = None  # Elapsed time (in seconds) since the client began the DHCP process.
    flags = None  # Broadcast bit (set to 1 to indicate message is broadcast)
    ciaddr = None  # Client IP Address (set by the client)
    yiaddr = None  # Your IP Address (set by the server to inform client the assigned IP address in Offer Message)
    siaddr = None  # IP address of the next server to use in the configuration and bootstrap process
    giaddr = None  # Relay Agent IP Address
    chaddr = None  # Client's hardware address (Layer 2 MAC address)
    sname = None  # Next Server (name of the next server for client to use in the configuration process)
    file = None  # Name of the file to request from Next Server (example: name of OS file)
    """DHCP Option Field"""
    msg_type = None
    option = MessageOptionFields(msg_type)

    def __init__(self, op, ciaddr, yiaddr, chaddr, msg_type):
        self.op = op
        self.htype = 1
        self.hlen = 6
        self.hops = 0
        self.xid = xid_generator()
        self.secs = 0
        self.flags = 1
        self.ciaddr = ciaddr
        self.yiaddr = yiaddr
        self.siaddr = IPAddress('0.0.0.0')
        self.giaddr = IPAddress('0.0.0.0')
        self.chaddr = chaddr
        self.sname = 'NoName'
        self.file = 'NoFile'
        self.define_msg_type(msg_type)

    def define_msg_type(self, msg_type):
        self.option.msg_type = msg_type

    def __str__(self):
        result = str(self.op) + " " + str(self.htype) + " " + str(self.hlen) + " " + str(self.hops) + " " + \
                 str(self.xid) + " " + str(self.secs) + " " + str(self.flags) + " " + str(self.ciaddr) + " " + \
                 str(self.yiaddr) + " " + str(self.siaddr) + " " + str(self.giaddr) + " " + \
                 str(self.chaddr) + " " + str(self.sname) + " " + str(self.file) + " " + \
                 str(self.option.msg_type) + " " + str(self.option.mask) + " " + str(self.option.cid) + " " +\
                 str(self.option.req_addr) + " " + str(self.option.hname) + " " +\
                 str(self.option.parreqlist) + " " + str(self.option.sid) + " " + \
                 str(self.option.router) + " " + str(self.option.dns) + " " + str(self.option.renewtime) + " " + \
                 str(self.option.rebindtime) + " " + str(self.option.leasetime)
        return result
