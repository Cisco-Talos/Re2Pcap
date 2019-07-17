#!/usr/bin/python3

'''
    Re2Pcap - Create Pcap from Raw HTTP Request or Response in seconds
    Copyright (C) 2019 Cisco Talos

    Author: Amit N. Raut

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

# Flask based web UI wrapper for Re2Pcap
from flask import render_template, Flask, request, url_for, redirect, send_file
from datetime import datetime
import os, subprocess, time, socket

app = Flask("Re2Pcap")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createPcap', methods=["POST"])
def createPcap():
    inputText = request.form['inputText']
    # if request.form['requestType'] == 'request':
    if len(inputText):
        # Write request from the textarea to file
        reqFile = os.path.join(os.getcwd(), 'io/', str(datetime.now()).replace(' ', '-') + '.req')
        f = open(reqFile, 'w+')
        f.write(inputText)
        f.close()
        # Create command to be passed to the req2pcap
        command = os.path.join(os.getcwd(), 'Re2Pcap') + ' ' + reqFile
    else:
        command = 'fail'
    try:
        if len(command) > 5:
            childProc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            time.sleep(5)
            childProc.communicate()
            if not childProc.returncode:
                resultFileName = request.form['pcapFileName'] + '.pcap' if request.form[
                    'pcapFileName'] else 'Re2Pcap-Result.pcap'
                return send_file(reqFile + '-result.pcap', as_attachment=True, attachment_filename=resultFileName)
            else:
                return '<h3>Something went Wrong :( Please Check the Input/ Error log and Try Again ....</h3>'
        else:
            return '<h3>Something went Wrong :( Please Check the Input/ Error log and Try Again ....</h3>'
    except subprocess.CalledProcessError:
        return '<h3>Something went Wrong :( Please Check the Input/ Error log and Try Again ....</h3>'


if __name__ == '__main__':
    host_ip = socket.gethostbyname(socket.gethostname())
    app.run(host=os.getenv('IP', host_ip), port=int(os.getenv('PORT', 5000)), debug=True)
