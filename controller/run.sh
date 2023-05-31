#!/usr/bin/env bash

# Gemerate the certificates
cd ~/; openssl rand -writerand .rnd
# Check if the /controller/certs folder exists and create it if not

if [ ! -d "/controller/certs" ]; then
    mkdir /controller/certs
    # CA
    openssl genrsa -des3 -passout pass:antonio -out /controller/certs/ca.key 4096
    openssl req -new -x509 -days 365 -key /controller/certs/ca.key -out /controller/certs/ca.crt -passin pass:antonio -subj "/C=ES/ST=PA/L=A/O=Uniovi/OU=SE/CN=sdp-controller/emailAddress=abc@xyz.com"
    # Controller
    openssl genrsa -out /controller/certs/controller.key 4096
    openssl req -new -key /controller/certs/controller.key -out /controller/certs/controller.csr -passin pass:antonio -subj "/C=ES/ST=PA/L=A/O=Uniovi/OU=SE/CN=sdp-controller/emailAddress=abc@xyz.com"
    openssl x509 -req -in /controller/certs/controller.csr -CA /controller/certs/ca.crt -CAkey /controller/certs/ca.key -CAcreateserial -out /controller/certs/controller.crt -days 365 -sha256 -passin pass:antonio
    # Gateway
    mkdir /controller/certs/clients
    openssl genrsa -out /controller/certs/clients/gateway.key 4096
    openssl req -new -key /controller/certs/clients/gateway.key -out /controller/certs/clients/gateway.csr -passin pass:antonio -subj "/C=ES/ST=PA/L=A/O=Uniovi/OU=SE/CN=sdp-gateway/emailAddress=abc@xyz.com"
    openssl x509 -req -in /controller/certs/clients/gateway.csr -CA /controller/certs/ca.crt -CAkey /controller/certs/ca.key -CAcreateserial -out /controller/certs/clients/gateway.crt -days 365 -sha256 -passin pass:antonio
    # Client
    openssl genrsa -out /controller/certs/clients/client.key 4096
    openssl req -new -key /controller/certs/clients/client.key -out /controller/certs/clients/client.csr -passin pass:antonio -subj "/C=ES/ST=PA/L=A/O=Uniovi/OU=SE/CN=sdp-client/emailAddress=abc@xyz.com"
    openssl x509 -req -in /controller/certs/clients/client.csr -CA /controller/certs/ca.crt -CAkey /controller/certs/ca.key -CAcreateserial -out /controller/certs/clients/client.crt -days 365 -sha256 -passin pass:antonio
fi


# Run the controller
cd /controller
#python3 controller.py
while true; do
    sleep 100
done