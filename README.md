<h1 align = "center"> Semi-automatic ARP SPOOFING with PYTHON </h1>

#### Hello guys,

This is my own project, which implements semi-automatic ARP-spoofing.

This material was created for informational purposes.
The information is provided solely for the purpose of familiarization.
The author strongly condemns any kind of hacker attacks and encourages to pay attention to security problems.

First of all, we find the network participants, using arp requests we find out their mac addresses ('Who it is').
Then, in fact, a MITM attack is carried out on some user of our network (we will call him target).
There is a substitution of IP and MAC in the target and gateway ARP tables, after which all traffic passes through us.
Then, thanks to sniffer (which is embedded in the code), we can view this traffic.
Additional filters and decoders are also implemented, which simplify the work with traffic and our lives :)
... Many thanks to the scapy module for almost all the work done for us.
