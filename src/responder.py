# responder.py

import os

WHITELIST = ["192.168.56.1"]

def block_ip(ip):

    if ip in WHITELIST:
        return

    os.system(f"iptables -I INPUT -s {ip} -j DROP")
