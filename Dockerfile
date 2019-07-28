FROM alpine

# Get required dependencies and setup for Re2Pcap
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update && apk add python3 tcpdump tcpreplay
RUN pip3 install --upgrade pip
RUN pip3 install pexpect flask requests httpretty 

COPY Re2Pcap/ /Re2Pcap
RUN cd Re2Pcap && chmod +x Re2Pcap.py

WORKDIR /Re2Pcap
EXPOSE 5000/tcp

# Run application at start of new container
CMD ["/usr/bin/python3", "Re2Pcap.py"]