from netaddr import *
from DHCP.Util.msg import *


def msg_decoder(msg):
    delimiter = " "
    temp = msg.split(delimiter)
    op = temp[0]
    htype = int(temp[1])
    hlen = int(temp[2])
    hops = int(temp[3])
    xid = int(temp[4])
    secs = int(temp[5])
    flags = int(temp[6])
    ciaddr = IPAddress(temp[7])
    yiaddr = IPAddress(temp[8])
    siaddr = IPAddress(temp[9])
    giaddr = IPAddress(temp[10])
    chaddr = temp[11]
    sname = temp[12]
    file = temp[13]
    msg_type = temp[14]
    mask = IPAddress(temp[15])
    cid = temp[16]
    req_addr = IPAddress(temp[17])
    hname = temp[18]
    parreqlist = temp[19]
    sid = temp[20]
    router = temp[21]
    dns = IPAddress(temp[22])
    renewtime = temp[23]
    rebindtime = temp[24]
    leasetime = temp[25]
    message = MessageFormat(op, ciaddr, yiaddr, chaddr, msg_type)
    message.htype = htype
    message.hlen = hlen
    message.hops = hops
    message.xid = xid
    message.secs = secs
    message.flags = flags
    message.siaddr = siaddr
    message.giaddr =giaddr
    message.sname = sname
    message.file = file
    message.option.mask = mask
    message.option.cid = cid
    message.option.req_addr = req_addr
    message.option.hname = hname
    message.option.parreqlist = parreqlist
    message.option.sid = sid
    message.option.router = router
    message.option.dns = dns
    message.option.renewtime = renewtime
    message.option.rebindtime = rebindtime
    message.option.leasetime = leasetime
    return message
