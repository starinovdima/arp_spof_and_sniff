import os
import socket as sock
import struct
import subprocess
import time
import ipaddress

from prettytable import PrettyTable
from socket import socket, AF_INET, SOCK_DGRAM
import scapy.all as scapy


def get_local_ip():
    st = socket(AF_INET, SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip_l = st.getsockname()[0]
    except Exception:
        ip_l = '127.0.0.1'
    finally:
        st.close()
    return ip_l


def get_gateway_ip():
    com = 'route -n'.split()
    ip_route = str(subprocess.check_output(com, shell=True)).split("\\n")[2].split()[1].strip()
    if ip_route.isdigit():
        return ip_route
    else:
        try:
            sock_ = sock.gethostbyname(ip_route)
            return sock_
        except BaseException:
            return os.popen("ip r | grep default").read().split()[2]


def output_mac_ip_table(mac_ip_list):
    th = ['IP Address', 'MAC Address']
    table = PrettyTable(th)
    columns = len(th)
    for row in mac_ip_list:
        table.add_row(row[:columns])
    print(table)


def get_ip_mac_addr(ip):

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast,iface='wlan0', timeout=3, verbose=False)[0]

    clients_list = []

    for element in answered_list:
        client_dict = [element[1].psrc, element[1].hwsrc]
        print(f"ip:{element[1].psrc} mac:{element[1].hwsrc}")
        clients_list.append(client_dict)
    return clients_list


def generate_ip(local_ip, prefix):
    return f'{local_ip.split(".")[0]}.{local_ip.split(".")[1]}.{local_ip.split(".")[2]}.' + str(prefix)


# def update_ip_table():
#   while True:

def get_prefix(local_ip):
    prefix = 0
    netmask = os.popen(f"ifconfig | grep {local_ip}").read().split()[3].split(".")
    for i in range(len(netmask)):
        prefix += str(bin(int(netmask[i]))).count("1")
    return '/' + str(prefix)
def main():
    #if not os.getuid() == 0:
      #  print("\n----------- Please, run with SUDO ! -----------")
      #  return
    print("----- Choose interface ( default: wlan0) ----- ")
    interface = input("---> ")
    if ( len(interface) == 0):
        interface = "wlan0"
    local_ip = get_local_ip()
    gateway_ip = get_gateway_ip()
    prefix = get_prefix(local_ip)
    #print(generate_ip(local_ip))
    while True:
        print(f"\n----------- Your local IP is  -->  {local_ip+prefix} ----------- ")
        print(f"----------- Gateway  IP  is   -->  {gateway_ip}  -----------")
        for i in (0,126):
            mac_ip_list = get_ip_mac_addr(generate_ip(local_ip,126))
        if not (len(mac_ip_list) == 0):
            output_mac_ip_table(mac_ip_list)
        print("\n- Please select target ip or update table(enter 'up') -")
        answer = input("---> ")
        if not "up" in answer:
            break


if __name__ == '__main__':
    main()
