# Re2Pcap: Create PCAP file from raw HTTP request or response in seconds

Re2Pcap is abbreviation for Request2Pcap and Response2Pcap. Community users can create PCAP file using Re2Pcap and test them against [Snort](https://snort.org) rules.

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
docker run --rm --cap-add NET_ADMIN -p 5000:5000 re2pcap
```
Open `localhost:5000` in your web browser to access Re2Pcap 


## Requirements

* Docker
* HTTP Raw Request / Response
* Web Browser (for best results, please use **_Chromium_** based web browsers) 

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

<img src='/Re2Pcap/static/img/Re2Pcap_Demo.gif' title='Re2Pcap Demo' width='' alt='Re2Pcap Demo Walkthrough' />

## Re2Pcap Development (dev) branch (Under Development)

Currently Re2Pcap dev branch has following additional functionality
* Simulated raw HTTP request and response to PCAP
* Better input validation

Here is video walkthrough of PCAP creation for [Sierra Wireless AirLink ES450 ACEManager iplogging.cgi command injection vulnerability](https://www.talosintelligence.com/reports/TALOS-2018-0746) using Re2Pcap **dev**

<img src='/Re2Pcap/static/img/Re2Pcap-Dev_Demo.gif' title='Re2Pcap Demo' width='' alt='Re2Pcap Demo Walkthrough' />

## Re2Pcap Workflow

<img src='/Re2Pcap/static/img/workflow.png' title='Re2Pcap Workflow' width='' alt='Re2Pcap Workflow' />

As shown in the above image Re2Pcap is Alpine Linux based Python3 application with Flask based web interface 

Re2Pcap parses the input data as raw HTTP request or response and actually perfoms client/server interaction while capturing packets. After the interaction Re2Pcap presents the captured packets as PCAP file

## Recommendations

* Please use Linux as your host operating system as Re2Pcap is well tested on Linux
* If creating PCAP for `Host: somedomain:5000`, please change Flask application to run on other port by modifying Re2Pcap.Py `app.run` call otherwise PCAP will contain Flask application response

---

I hope you find Re2Pcap helpful. If you face issues with Re2Pcap please create an issue with your inputs. Thank you! :)

**Enjoy** 😊
