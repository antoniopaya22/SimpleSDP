FROM ubuntu:18.04

EXPOSE 5000

WORKDIR /controller

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install Python3 and dependencies
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip openssl libssl-dev libffi-dev
RUN pip3 install --upgrade pip

COPY ./requirements.txt /controller/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /controller

CMD ["/bin/bash","-c", " ./run.sh"]