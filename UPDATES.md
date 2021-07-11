## Updates file to track changes to Re2Pcap development

### Update 07/11/2021
- Fixed encoding problem. Everything is now treated as UTF-8.

### Update 06/16/2020
- Fixed `pip3 not found` error by adding `py3-pip` along with python3 

### Update 04/14/2020
- Added simplifid installation of `Re2Pcap` using [re2pcap.sh](./re2pcap.sh). Now users just need to run `./re2pcap.sh` after navigating to cloned git repo to run `Re2Pcap`

### Update 08/19/2019

* Updated README.md
    - Added new walkthrough GIF images
    - Updated usage section with one liner `docker run` command
    - Fixed typo

### Update 08/05/2019

* Updated Re2Pcap-cmd script
    - Changed usage message
    - Added ASCII art for Re2Pcap banner
    - Changed displaying of error messages

### Update 08/04/2019

* Integradted simulated raw request and response to PCAP in master
    - Simulated request to response can be ideal to simulate Malware C2 traffic
* PCAP file are now on different source and desination IP (fix for [issue](https://github.com/Cisco-Talos/Re2Pcap/issues/3))
    - Source IP: 10.10.10.1 (Add-on IP added and removed using `ip addr add/del 10.10.10.1 dev eth0`) 
    - Destination IP: 172.17.0.2
* Changes to UI
    - Fixed minimum height of `53vh` for textareas
    - @route /validate is called on content change of either of the textareas
    - Result of /validate shows if input is parsable or not. UI elements are enabled and disabled based on /validate result
