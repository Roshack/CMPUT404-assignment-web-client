#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Rob Hackman
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body="",data=""):
        self.code = code
        self.body = body
        self.data = data
    def __str__(self):
        return str(self.data)

class HTTPClient(object):
    #def get_host_port(self,url):
        

    def connect(self, host, port):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print "Failed to create socket. Error code: " + str(msg[0]) +' , Err Message'
            sys.exit();
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            print "Hostname: '%s' could not be resolved. Exitting" % host
            sys.exit()
        s.connect((ip,port))
        return s

    def get_code(self, data):
        templist = data.split("\r\n\r\n")
        code = re.match("HTTP/1.[0-1] (\d*) .*\r\n",templist[0]).group(1)
        return int(code)
    
    def get_headers(self,data):
        return None

    def get_body(self, data):
        templist = data.split("\r\n\r\n")
        if len(templist) >= 2:    
            return templist[1]
        return ""

    # read everything from the socket
    def recvall(self, sock):
        buff = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buff.extend(part)
            else:
                done = True
        return str(buff)

    def GET(self, url, args=None):
        #code = 500
        #body = "GET / HTTP/1.1\r\nUser-Agent: robconnect\r\nHost: %s\r\nAccept: */*\r\n\r\n" % url
        parsed = urlparse(url)
        port = 80
        if (parsed.port):
            port = parsed.port
        path = "/"
        host = url
        if parsed.hostname:
            host = parsed.hostname
        if parsed.path:
            path = parsed.path
        sock = self.connect(host,port)
        msg = "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n" % (path,host)
        try:
            sock.sendall(msg)
        except socket.error:
            print "GET send failed"
            sys.exit()
        data = self.recvall(sock)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPRequest(code, body,data)

    def POST(self, url, args=None):
        code = 500
        parsed = urlparse(url)
        port = 80
        if (parsed.port):
            port = parsed.port
        path = "/"
        host = url
        if parsed.hostname:
            host = parsed.hostname
        if parsed.path:
            path = parsed.path
        sock = self.connect(host,port)
        if (args != None):
            params = urllib.urlencode(args)
            msg = "POST %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n"% (path,host)
            msg += "Content-Type: application/x-www-form-urlencoded\r\n"
            msg += "Content-Length: %d\r\n\r\n%s" % (len(params),params)
        else:
            msg = "POST %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n" % (path,host)
        try:
            sock.sendall(msg)
        except socket.error:
            print "POST send failed"
            sys.exit()
        data = self.recvall(sock)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1],command )    
