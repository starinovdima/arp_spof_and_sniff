import os
import socket as sock
import struct
import subprocess
import time

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
        sock_ = sock.gethostbyname(ip_route)
        return sock_


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
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,
                              verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = [element[1].psrc, element[1].hwsrc]
        clients_list.append(client_dict)
    return clients_list


def generate_ip(local_ip, prefix):
    return f'{local_ip.split(".")[0]}.{local_ip.split(".")[1]}.{local_ip.split(".")[2]}.1' + prefix


# def update_ip_table():
#   while True:

def get_prefix(local_ip):
    return '/' + os.popen(f"ip a | zgrep {local_ip}").read().split()[1].split("/")[1]


def main():
    if not os.getuid() == 0:
        print("\n----------- Please, run with SUDO ! -----------")
        return
    local_ip = get_local_ip()
    gateway_ip = get_gateway_ip()
    prefix = get_prefix(local_ip)
    while True:
        print(f"\n----------- Your local IP is  -->  {local_ip} ----------- ")
        print(f"----------- Gateway  IP  is   -->  {gateway_ip}  -----------")
        mac_ip_list = get_ip_mac_addr(generate_ip(local_ip, prefix))
        if not (len(mac_ip_list) == 0):
            output_mac_ip_table(mac_ip_list)
        print("\n- Please select target ip or update table(enter 'up') -")
        answer = input()
        if not "up" in answer:
            break


if __name__ == '__main__':
    main()
