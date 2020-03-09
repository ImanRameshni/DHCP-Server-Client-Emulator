def client_log_ip(ip_add, mask, dgw, dns):
    ip_init_text = 'IP: ', str(ip_add), '\n'
    mask_init_text = 'Subnet Mask: ', str(mask), '\n'
    dgw_init_text = 'Default Gateway: ', str(dgw), '\n'
    pref_dns_init_text = 'DNS Server: ', str(dns), '\n'

    file = open("client_log.txt", "a+")
    file.writelines(ip_init_text)
    file.writelines(mask_init_text)
    file.writelines(dgw_init_text)
    file.writelines(pref_dns_init_text)
    file.close()


def client_log_stat(message):
    status = 'Status: ', str(message), '\n'

    file = open("client_log.txt", "a+")
    file.writelines(status)
    file.close()


def client_log(message):
    file = open("client_log.txt", "a+")
    file.writelines(message + '\n')
    file.close()


def server_log_ip(dns_ip, dgw_ip, netmask, ip_pool_first, ip_pool_last):
    pref_dns_text = 'DNS Server: ', str(dns_ip), '\n'
    dgw_ip_text = 'Default Gateway: ', str(dgw_ip), '\n'
    netmask_text = 'Subnet Mask: ', str(netmask), '\n'
    pool_text = 'IP Pool: ', str(ip_pool_first), ' - ', str(ip_pool_last), '\n'

    file = open("server_log.txt", "a+")
    file.writelines(dgw_ip_text)
    file.writelines(netmask_text)
    file.writelines(pref_dns_text)
    file.writelines(pool_text)
    file.close()


def server_log_stat(message):
    status = 'Status: ', str(message), '\n'

    file = open("server_log.txt", "a+")
    file.writelines(status)
    file.close()


def server_log(message):
    file = open("server_log.txt", "a+")
    file.writelines(message + '\n')
    file.close()


def server_log_assigned_ip_addr(message):
    file = open("assigned_ip_addresses.txt", "a+")
    file.writelines(message + '\n')
    file.close()


def client_log_divider():
    client_log("*****************************************************************")


def server_log_divider():
    server_log("*****************************************************************")


def server_log_assigned_ip_divider():
    server_log_assigned_ip_addr("*****************************************************************")