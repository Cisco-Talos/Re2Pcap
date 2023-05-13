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
import os, subprocess, time, socket, httpretty
from flask import jsonify

from io import BytesIO, StringIO

from http.client import HTTPResponse

app = Flask("Re2Pcap")

@app.route('/')
def index():
    return render_template('index.html')


# Fake socket class for http response parsing
class FakeSocket():
	def __init__(self, response_str):
		self._file = BytesIO(response_str)
	def makefile(self, *args, **kwargs):
		return self._file


# Function to parse HTTP Response and return response object
def parse_Response(res_file):
	try:
		response_str = res_file
		source = FakeSocket(response_str.encode('utf-8'))
		response = HTTPResponse(source)
		response.begin()
		# response_body = response.read()
	except Exception as e:
		return {"error": "Failed to Parse Given HTTP Raw Response. Please Verify your Input and Try Again."}
	return response


# Function to parse HTTP Request and return (req, port, postParam)
def parse_Request(req_file):
	try:
		# Parse the HTTP raw request in terms of headers, URI, client body
		req = httpretty.core.HTTPrettyRequest(req_file)
		if req.error_code == 400:
			logger.error(req.error_message)
		else:
			# Get POST parameter values. Httpretty parsing of post param adds `\n\r\n\r` so getting rid of last 4 bytes
			postParam = str(req.rfile.read(), 'utf-8')[:-2]
			# if not req.headers['host']:
			# 	logger.error(' Please Add Host Request Header')
			if ':' in req.headers['host']:
				port = int(req.headers['host'][req.headers['host'].index(':') + 1:])
			else:
				port = 80
	except Exception as e:
		return {"error": "Failed to Parse Given HTTP Raw Request. Please Verify your Input and Try Again."}
	return req, port, postParam


# Route to validate the input raw request or response before sending it for /createPcap route
@app.route('/validate', methods=["POST"])
def validate():
	inputRequest = request.form['inputRequest']
	inputResponse = request.form['inputResponse']
	
	# Try to parse the input Request and Response and respond via Ajax before processing input via Re2Pcap script
	is_request_parsable = parse_Request(inputRequest)
	is_response_parsable = parse_Response(inputResponse)

	if not len(inputRequest) and not len(inputResponse):
		return jsonify(error="Please input request or response....")
	elif (len(inputRequest) and isinstance(is_request_parsable, dict)):
		return jsonify(error="Request is not parsable. Please try again....")
	elif (len(inputResponse) and isinstance(is_response_parsable, dict)):
		return jsonify(error="Response is not parsable. Please try again....")
	else:
		return jsonify(success="Woot! Input looks good!")


# Route to create command to generate PCAP from Re2Pcap core script and serve the generated PCAP to user
@app.route('/createPcap', methods=["POST"])
def createPcap():
	inputRequest = request.form['inputRequest']
	inputResponse = request.form['inputResponse']
	resultFileName = request.form['pcapFileName'] + '.pcap' if request.form['pcapFileName'] else 'Re2Pcap-Result.pcap'

	if len(inputRequest):
	# Write request from the textarea to file
		reqFile = os.path.join(os.getcwd(), 'io/Request.req')
		f = open(reqFile, 'w+')
		f.write(inputRequest)
		f.close()
		command = os.path.join(os.getcwd(), 'Re2Pcap') + ' ' + reqFile
	else:
		command = os.path.join(os.getcwd(), 'Re2Pcap') + ' ' + "NO"

	if len(inputResponse):
		# Write Response from the textarea to file
		resFile = os.path.join(os.getcwd(), 'io/Response.res')
		f = open(resFile, 'w+')
		f.write(inputResponse)
		f.close()
		command += ' ' + resFile
	else:
		command += ' ' + "NO"
	
	try:
		if len(command) > 5:
			childProc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			time.sleep(5)
			childProc.communicate()
			if not childProc.returncode:
				return send_file('io/Re2Pcap-result.pcap', as_attachment=True, download_name=resultFileName)
			else:
				return jsonify(error='Something went Wrong :( Please Check the Input/ Error log and Try Again ....')
		else:
			return jsonify(error='Something went Wrong :( Please Check the Input/ Error log and Try Again ....')
	except subprocess.CalledProcessError:
		return jsonify(error='Something went Wrong :( Please Check the Input/ Error log and Try Again ....')


if __name__ == '__main__':
	host_ip = socket.gethostbyname(socket.gethostname())
	app.run(host=os.getenv('IP', host_ip), port=int(os.getenv('PORT', 5000)), debug=True)
