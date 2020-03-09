from netaddr import *


class IPPool:
    ip_range = IPRange('192.168.1.3', '192.168.1.100')
    ip_pool = iter_iprange(ip_range.first, ip_range.last, step=1)
    assigned_list = []
    # assigned_list.append(IPAddress('192.168.1.4'))

    def assign_ip(self):
        user_ip = self.ip_pool.__next__()
        print(user_ip)
        available = self.is_ip_available(user_ip)
        if available:
            self.assigned_list.append(user_ip)
            return user_ip
        else:
            return IPAddress('0.0.0.0')

    def get_first(self):
        return self.ip_range.first

    def get_last(self):
        return self.ip_range.last

    def is_ip_available(self, offered_ip):
        if offered_ip not in self.assigned_list:
            return True
        else:
            return False
