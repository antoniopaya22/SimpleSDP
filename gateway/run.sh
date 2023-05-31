#!/usr/bin/env bash

# Flush existing rules and chains
iptables -F
iptables -X

# Set default policies to DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback traffic
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related incoming connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow outbound DNS queries
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow outbound HTTP/HTTPS traffic
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 5000 -j ACCEPT
iptables -A OUTPUT -p udp --dport 5000 -j ACCEPT

# Log and drop all other incoming traffic
iptables -A INPUT -j LOG --log-prefix "DROP: "
iptables -A INPUT -j DROP

yes Y  | cp config/access.conf /etc/fwknop/
yes Y  | cp config/fwknopd.conf /etc/fwknop/

#fwknopd -f

# Start the Apache service in the background
service apache2 start

while true; do
    sleep 100
done