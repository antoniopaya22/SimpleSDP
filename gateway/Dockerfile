FROM ubuntu:18.04

EXPOSE 4444

WORKDIR /gateway

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

USER root

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y make automake curl git net-tools conntrack openssl libssl-dev libjson-c-dev libpcap-dev texinfo libtool autoconf libuv1 libuv1-dev
RUN apt-get install -y iptables
RUN apt-get install -y apache2

# Install FWKNOP
RUN git clone https://github.com/mrash/fwknop
RUN cd fwknop && libtoolize --force && aclocal && autoheader && automake --force-missing --add-missing && autoconf
RUN cd fwknop && ./configure --disable-client --prefix=/usr --sysconfdir=/etc && make && make install

# Install Python3 and dependencies
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip openssl libssl-dev libffi-dev
RUN pip3 install --upgrade pip
RUN apt install -y nano wireshark

COPY ./requirements.txt /gateway/requirements.txt
RUN pip3 install -r /gateway/requirements.txt

# Copy configuration files
COPY . .

CMD ["/bin/bash","-c", " ./run.sh $SERVER_HOSTNAME"]