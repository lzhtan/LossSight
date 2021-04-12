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
Total_Loss_Bit = 0

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
                    BitField("loss_bit", 0, 8),
                    BitField("count", 0, 8),
                    PacketListField("swtraces",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt:(pkt.count*1)) ]

def handle_pkt(pkt):

    #print "got a packet"
    #pkt.show2()
    f=open('telemetry(lossrate=0.003).txt','a')
    timenow = time.strftime('%Y-%m-%d %H:%M:%S')
    f.writelines([timenow, str(pkt[IP].options),'\n'])
    print(str(pkt[IP].options))

    sys.stdout.flush()




def main():
    iface = 'h2-eth0'
    print "sniffing on %s" % iface
    sys.stdout.flush()
    sniff(filter="udp and port 4321", iface = iface,
          prn = lambda x: handle_pkt(x))





if __name__ == '__main__':
    main()
