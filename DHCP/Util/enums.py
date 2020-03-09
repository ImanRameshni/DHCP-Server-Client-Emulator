import enum


class MessageType(enum.Enum):
    type1 = "DHCPDISCOVER"
    type2 = "DHCPOFFER"
    type3 = "DHCPREQUEST"
    type4 = "DHCPACK"
    type5 = "DHCPNACK"


class OperationCode(enum.Enum):
    operation1 = "REQUEST"
    operation2 = "REPLY"
