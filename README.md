## Re2Pcap: Create PCAP file from raw HTTP request or response in seconds
<img src='https://img.shields.io/static/v1?label=Python3&message=Requests%20|%20Flask%20|%20Pexpect%20|%20Http.server%20|%20Http.client%20|%20Httpretty&color=blue' title='Shields'/> <img src='https://img.shields.io/static/v1?label=&message=Snort%20|%20Docker%20|%20Alpine%20Linux%20%20|%20PCAP%20|%20Tcpdump%20&color=success' title='Shields'/>


<img src='/Re2Pcap/static/img/re2pcap.png' title='Re2Pcap Logo'/>

Re2Pcap is abbreviation for Request2Pcap and Response2Pcap. Community users can quickly create PCAP file using Re2Pcap and test them against [Snort](https://snort.org) rules.

Re2Pcap allow you to quickly create PCAP file for raw HTTP request shown below 
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

### Usage

```
git clone https://github.com/Cisco-Talos/Re2Pcap.git
cd Re2Pcap/
./re2pcap.sh
```
OR
```
docker run --rm --cap-add NET_ADMIN -p 5000:5000 --name re2pcap amitraut/re2pcap
```

Open `localhost:5000` in your web browser to access Re2Pcap or use [Re2Pcap-cmd](Re2Pcap-cmd) script to interact with Re2Pcap container to get PCAP in current working directory 


### Requirements

* Docker
* HTTP Raw Request / Response
* Web Browser (for best results, please use **_Chromium_** based web browsers) 

### Advantages

* Easy setup. No complex multi-VM setup required
* Re2Pcap runs on Alpine Linux based docker image that weighs less than 100 MB :D
* Allows you to dump simulated raw HTTP request and response in to PCAP

### Dockerfile

```
FROM alpine

# Get required dependencies and setup for Re2Pcap
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update && apk add python3 tcpdump tcpreplay
RUN pip3 install --upgrade pip
RUN pip3 install pexpect flask requests httpretty requests-toolbelt

COPY Re2Pcap/ /Re2Pcap
RUN cd Re2Pcap && chmod +x Re2Pcap.py

WORKDIR /Re2Pcap
EXPOSE 5000/tcp

# Run application at start of new container
CMD ["/usr/bin/python3", "Re2Pcap.py"]
```

### Walkthrough

* Video walkthrough shows pcap creation for Sierra Wireless AirLink ES450 ACEManager iplogging.cgi [command injection vulnerability](https://www.talosintelligence.com/reports/TALOS-2018-0746) using Re2Pcap web interface

<img src='/Re2Pcap/static/img/Re2Pcap_Demo.gif' title='Re2Pcap Demo' alt='Re2Pcap Demo Walkthrough' />

* Video walkthrough of PCAP creation for Sierra Wireless AirLink ES450 ACEManager iplogging.cgi [command injection vulnerability](https://www.talosintelligence.com/reports/TALOS-2018-0746) using Re2Pcap-cmd script

<img src='/Re2Pcap/static/img/Re2Pcap_Demo1.gif' title='Re2Pcap-cmd Demo' alt='Re2Pcap-cmd Demo'/>

### Re2Pcap Workflow

<img src='/Re2Pcap/static/img/workflow.png' title='Re2Pcap Workflow' alt='Re2Pcap Workflow'/>

As shown in the above image Re2Pcap is Alpine Linux based Python3 application with Flask based web interface 

Re2Pcap parses the input data as raw HTTP request or response and actually perfoms client/server interaction while capturing packets. After the interaction Re2Pcap presents the captured packets as PCAP file

### Recommendations

* Please use Linux as your host operating system as Re2Pcap is well tested on Linux
* If creating PCAP for `Host: somedomain:5000` i.e. port 5000, please change Flask application to run on other port by modifying Re2Pcap.Py `app.run` call otherwise PCAP will contain Flask application response

### Limitations

* If raw HTTP request is without `Accept-Encoding:` header `Accept-Encoding: identity` is added in the reqeust
    - There is known [issue](https://github.com/psf/requests/issues/2234) for it in python requests. Following is closing note for that issue 
    > That's really fairly terrible. Accept-Encoding: identity is always valid, the RFCs say so. It should be utterly harmless to send it along. Otherwise, removing this requires us to replace httplib. That's a substantial bit of work. =(

* The following are source and destination IPs in PCAPs from Re2Pcap
    - Source IP: 10.10.10.1
    - Destination IP: 172.17.0.2 or (Re2Pcap Container's IP Address)
    
    Please use `tcprewrite -D` option to modify desitnation IP to something else as per your need. You may also use `tcpprep` and `tcprewrite` to set other IPs as endpoints. Due to inconsistent result of `tcprewrite` I used alternative way to set different SRC/DST IPs

* Specifying `HTTP/1.1 302 FOUND` as response will generated PCAP with maximum possible retries to reach resource specified in `Location:` header. Plase export the first HTTP stream using wireshark in testing if you do not like the additional noise of other streams

---

I hope you find Re2Pcap helpful. If you face issues with Re2Pcap please create an issue with your inputs. Thank you! :)

**Enjoy** 😊
