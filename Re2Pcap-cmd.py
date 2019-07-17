#!/usr/bin/env python3

import requests, logging, sys, os

# Define logger and logLevel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def usage():
    print("\nUsage: Re2Pcap-cmd.py <Request/Response file> <PCAP file name (optional)>\n")


def main():

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    else:
        requestFile = sys.argv[1]
        if len(sys.argv) == 3:
            pcapName = sys.argv[2]
        else:
            pcapName = "Re2Pcap-Result"
        
        # Make request to Re2Pcap container running at localhost:5000. Please change this if container is running on different IP/port
        url = "http://localhost:5000/createPcap"
        data = {"inputText": open(requestFile).read(), "pcapFileName": pcapName, "submit":""}

        try:
            response = requests.post(url, data=data, stream=True)
            if response.status_code == 200:
                with open(os.path.join(os.getcwd(),"{}.pcap".format(pcapName)), "wb") as wfile:
                    for chunk in response.iter_content(chunk_size=8192):
                        wfile.write(chunk)
                logger.info(" \nPCAP file is stored as {}.pcap.\nThank you for using Re2Pcap :)".format(pcapName))
        except requests.exceptions.RequestException as e:
            logger.error(" \nFailed to send request to Re2Pcap container :( Please try again....\n{}".format(e))


if __name__=="__main__":
    main()

