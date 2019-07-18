# Re2Pcap: Create PCAP file from raw HTTP request or response in seconds

Re2Pcap is abbreviation for Request2Pcap and Response2Pcap. Community users can generate PCAP file using Re2Pcap and test them against [Snort](https://snort.org) rules.

Re2Pcap allow you to quickly create PCAP file for HTTP request shown below 
```
POST /admin/tools/iplogging.cgi HTTP/1.1
Host: 192.168.13.31:80
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/plain, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.13.31:80/admin/tools/iplogging.html
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 63
Cookie: token=1e9c07e135a15e40b3290c320245ca9a
Connection: close

tcpdumpParams=tcpdump -z reboot -G 2 -i eth0&stateRequest=start
```

## Usage

```
git clone https://github.com/Cisco-Talos/Re2Pcap.git
cd Re2Pcap/
docker build -t re2pcap .
docker run -ti --rm --cap-add NET_ADMIN -p 5000:5000 re2pcap 
```
Open localhost:5000 in your web browser to access Re2Pcap or use [Re2Pcap-cmd.py](Re2Pcap-cmd.py) script to interact with Re2Pcap container to get PCAP in current working directory


## Requirements

* Docker
* HTTP Raw Request / Response
* Web Browser (for best results, please use **_Chromium_** based web browsers) or if you prefer commandline you can use [Re2Pcap-cmd.py](Re2Pcap-cmd.py) script to generate PCAP in currrent working directory

## Advantages

* Easy setup. No complex multi-VM setup required
* Re2Pcap runs on Alpine Linux based docker image that weighs less than 90MB :p

## Dockerfile

```
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
```

## Walkthrough

* Video walkthrough shows pcap creation for [Sierra Wireless AirLink ES450 ACEManager iplogging.cgi command injection vulnerability](https://www.talosintelligence.com/reports/TALOS-2018-0746) using Re2Pcap

<img src='/Re2Pcap/Re2Pcap_Demo.gif' title='Re2Pcap Demo' width='' alt='Re2Pcap Demo Walkthrough' />

## References

* https://www.talosintelligence.com/reports/TALOS-2018-0746
* http://docs.python-requests.org/en/master/
* https://pexpect.readthedocs.io/en/stable/
* https://docs.docker.com/

---

I hope you find Re2Pcap helpful. If you face issues with Re2Pcap please create an issue with your input request or response. Thank you! :)

**Enjoy** 😃
