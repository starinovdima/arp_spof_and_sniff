import os
import socket as sock

from prettytable import PrettyTable
from socket import socket, AF_INET, SOCK_DGRAM
import scapy.all as scapy
import getmac.getmac as getmac
from scapy.layers.l2 import Ether, ARP


local_ip = ''
gateway_ip = ''
mac_ip_list = []

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
    #com = 'route -n'.split()
    #ip_route = str(subprocess.check_output(com, shell=True)).split("\\n")[2].split()[1].strip()
    ip_route = os.popen("ip r | grep default").read().split()[2]
    if ip_route.isdigit():
        return ip_route
    else:
        try:
            sock_ = sock.gethostbyname(ip_route)
            return sock_
        except BaseException:
            return os.popen("ip r | grep default").read().split()[2]


def output_mac_ip_table(mac_ip_list):
    th = ['IP Address','Wifi module name', 'MAC Address']
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

def ipneigh_ip_mac():
    list_ = os.popen("ip neigh").read().split("\n")
    ip_mac = []
    for i in range(len(list_)):
        if not (list_[i] == ''):
            ip_mac_list = [list_[i].split()[0], list_[i].split()[4]]
            ip_mac.append(ip_mac_list)
    return ip_mac

def generate_ip(local_ip, prefix):
    return f'{local_ip.split(".")[0]}.{local_ip.split(".")[1]}.{local_ip.split(".")[2]}.0/' + prefix

def scapy_arp(ip):
    ans_list = []
    ans = scapy.arping(ip, timeout=3, cache=0, verbose=False)[0]

    for s,r in ans.res:

        manuf = scapy.conf.manufdb._get_short_manuf(r.src)
        manuf = "unknown" if manuf == r.src else manuf
        ans_list.append((r[ARP].psrc, manuf, r[Ether].src))

    return ans_list

def get_accuracy(num,prefix):
    norm_n = 20
    count_by_prefix = (32 - prefix) / 10
    accuracy = norm_n * num // count_by_prefix
    return accuracy


def get_prefix(local_ip):
    prefix = 0
    netmask = os.popen(f"ifconfig | grep {local_ip}").read().split()[3].split(".")
    for i in range(len(netmask)):
        prefix += str(bin(int(netmask[i]))).count("1")
    return str(prefix)

def scan_network():

    if not os.getuid() == 0:
        print("\n----------- Please, run with SUDO ! -----------")
        return

    try:
        print("----- Choose interface ( default: wlan0) ----- ")
        interface = input("---> ")
        if ( len(interface) == 0):
            interface = "wlan0"

        local_ip = get_local_ip()
        gateway_ip = get_gateway_ip()
        prefix = get_prefix(local_ip)

        print("----- Enter search accuracy ( 0 < default 0.5 < 1) -----")
        accuracy = input("---> ")
        if (len(accuracy) == 0):
            accuracy = "0.5"
        accuracy = get_accuracy(float(accuracy),int(prefix))



        while True:
            print(f"\n----------- Your local IP is  -->  {local_ip}/{prefix} ----------- ")
            print(f"----------- Gateway  IP  is   -->  {gateway_ip}  -----------")

            for i in range(int(accuracy)):
                #mac_ip_l = get_ip_mac_addr(generate_ip(local_ip,prefix))  #1 way
                mac_ip_l = scapy_arp(generate_ip(local_ip,prefix))         #2 way
                print(f"---- {i+1} operation ----")
                if(len(mac_ip_l) > len(mac_ip_list)):
                    mac_ip_list = mac_ip_l
            neigh = ipneigh_ip_mac()
            if(len(mac_ip_list) < len(neigh)):
                mac_ip_list = neigh
            if not (len(mac_ip_list) == 0):
                output_mac_ip_table(mac_ip_list)

            print("\n- Do you want to continue or update table(enter 'up') -")
            answer = input("---> ")
            if not "up" in answer:
                break

    except BaseException:
        print("Oooops, something wrong...... ")

if __name__ == '__main__':
    scan_network()


