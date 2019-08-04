## Updates file to track changes to Re2Pcap development

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
