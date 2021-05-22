#!/usr/bin/env python
import sys
import struct
import time 

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import PacketListField, ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR

Total_Loss = 0.0
Total_Packet = 0.0
Total_Lost_Packet = 0.0
Total_Loss_Bit1 = 0
Total_Loss_Bit2 = 0

def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

class SwitchTrace(Packet):
    fields_desc = [ IntField("swid", 0),
                  IntField("qdepth", 0)]
    def extract_padding(self, p):
                return "", p

class IPOption_INT(IPOption):
    name = "INTLoss"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swtraces",
                                  adjust=lambda pkt,l:l*2+4),
                    BitField("loss_bit1", 0, 2),
		    BitField("loss_bit2", 0, 2),
                    BitField("count", 0, 12),
                    PacketListField("swtraces",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt:(pkt.count*1)) ]

def handle_pkt(pkt):
    global Total_Loss
    global Total_Packet
    global Total_Lost_Packet
    global Total_Loss_Bit1
    global Total_Loss_Bit2
    if Total_Packet%100 == 0:
        print("[Ordinary Report]")
        print("  - Event: Receive the #" + str(int(Total_Packet)) +" telemetry packet!")
        print("  - Telemetry Result Stream: " + str(IPOption_INT(str(pkt[IP].options))) + "\n")
        #pkt.show2()
    loss_bit1 = str(IPOption_INT(str(pkt[IP].options)))[77:78]
    loss_bit2 = str(IPOption_INT(str(pkt[IP].options)))[90:91]
    if (int(loss_bit1) != Total_Loss_Bit1):
        if (int(loss_bit2) != Total_Loss_Bit2):
	    Total_Packet = Total_Packet + 1
            Total_Lost_Packet = Total_Lost_Packet + 1
            Total_Loss_Bit1 = int(loss_bit1) + 1
            Total_Loss_Bit2 = int(loss_bit2) + 1
            print("[Warning]")
	    print("  - Packet Loss Happened!" )
	    print("[Detail]") 
            print("  - Time: " + time.strftime('%H:%M:%S',time.localtime(time.time())))
	    print("  - Location: Switch #2")
	    print("[More Information]") 
	    print("  - Cumulative number of Telemetry Reports: " + str(int(Total_Packet))) 
	    print("  - Cumulative number of Lost Packets: " + str(int(Total_Lost_Packet))) 
            print("  - Current Loss Rate: " + str(100*Total_Lost_Packet/Total_Packet)+ "\n")
        else:
	    Total_Packet = Total_Packet + 1
            Total_Lost_Packet = Total_Lost_Packet + 1
            Total_Loss_Bit1 = int(loss_bit1) + 1
            print("[Warning]")
	    print("  - Packet Loss Happened!" )
	    print("[Detail]")
	    print("  - Time: " + time.strftime('%H:%M:%S',time.localtime(time.time())))
	    print("  - Location: Switch #1")
	    print("[More Information]") 
	    print("  - Cumulative number of Telemetry Reports: " + str(int(Total_Packet))) 
	    print("  - Cumulative number of Lost Packets: " + str(int(Total_Lost_Packet))) 
	    print("  - Current Loss Rate: " + str(100*Total_Lost_Packet/Total_Packet)+ "%\n")
    else:
        Total_Packet = Total_Packet + 1
	Total_Loss_Bit1 = int(loss_bit1) + 1
        Total_Loss_Bit2 = int(loss_bit2) + 1

    if ( Total_Loss_Bit1 > 3):
        Total_Loss_Bit1 = 0
    if ( Total_Loss_Bit2 > 3):
        Total_Loss_Bit2 = 0

    sys.stdout.flush()




def main():
 
    iface = 'h2-eth0'

    print("\n")
    print("      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("      +    LossSight is Ready!    +")
    print("      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("\n")





    sys.stdout.flush()
    sniff(filter="udp and port 4321", iface = iface,
          prn = lambda x: handle_pkt(x))





if __name__ == '__main__':
    main()
