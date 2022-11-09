import os
import socket
import struct
import subprocess
import time
from prettytable import PrettyTable

from getmac.getmac import _get_default_iface_linux
from netifaces import ifaddresses, AF_INET
import scapy.all as scapy

def get_local_ip():
    try:
        return ifaddresses(_get_default_iface_linux()).setdefault(AF_INET)[0]['addr']
    except TypeError:
        return "127.0.0.1"

def get_gateway_ip():
    com = 'route -n'.split()
    ip_route = str(subprocess.check_output(com, shell=True)).split("\\n")[2].split()[1].strip()
    if ip_route.isdigit():
        return ip_route
    else:
        sock = socket.gethostbyname(ip_route)
        return sock

def output_mac_ip_table(mac_ip_list):
    th = ['IP Address', 'MAC Address']
    table = PrettyTable(th)
    columns = len(th)
    for row in mac_ip_list:
        table.add_row(row[:columns])
    print(table)


#def update_ip_table():




def main():
    #if not os.getuid() == 0:
     #   print("\n----------- Please, run with SUDO ! -----------")
     #   return
    local_ip = get_local_ip()
    gateway_ip = get_gateway_ip()
    print(f"\n----------- Your local IP is  -->  {local_ip} ----------- ")
    print(f"----------- Gateway  IP  is   -->  {gateway_ip}  -----------")
    output_mac_ip_table([[local_ip,gateway_ip],[local_ip,gateway_ip]])




if __name__ == '__main__':
    main()


