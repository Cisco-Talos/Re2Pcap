#!/bin/bash

#  Re2Pcap - Create Pcap from Raw HTTP Request or Response in seconds
#  Copyright (C) 2019 Cisco Talos
#
#  Author: Amit N. Raut
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

# Print banner
echo
echo "                 ╦═╗╔═╗┌─┐╔═╗╔═╗╔═╗╔═╗"
echo "                 ╠╦╝║╣ ┌─┘╠═╝║  ╠═╣╠═╝"
echo "                 ╩╚═╚═╝└─┘╩  ╚═╝╩ ╩╩ "

# Start animation for the text
animate()
{
   animation_text=( "| Please wait... | " "                   " )

   while :
   do
      for i in "${animation_text[@]}"
      do
         echo -en "\r$i"
         sleep 0.9
      done
   done
}

CONTAINER_RUNTIME=""

# Check to see if Docker is present on the system
if type docker >/dev/null 2>&1; then
  CONTAINER_RUNTIME="docker"
elif type podman >/dev/null 2>&1; then
  CONTAINER_RUNTIME="podman"
else 
  echo -e >&2 "\nNeither Docker nor Podman detected. One of them is required for Re2Pcap. Please install Docker or Podman first. Exiting..."
  exit 1
fi

# Check to see if `re2pcap` docker image is already present
if [[ "$(${CONTAINER_RUNTIME} images -q re2pcap:latest 2> /dev/null)" == "" ]]; then
   echo
   echo "Building Re2Pcap docker Image"
   animate &
   ANIMATE_ID=$!
   ${CONTAINER_RUNTIME} build -t re2pcap . > /dev/null
   kill -13 $ANIMATE_ID 
fi

echo
# Print instructions
echo -e "\n==> Now navigate to http:localhost:5000 or use 'Re2Pcap-cmd' to create PCAP. Thank you! :)\n" 

${CONTAINER_RUNTIME} run --rm --cap-add NET_ADMIN -p 5000:5000 re2pcap
