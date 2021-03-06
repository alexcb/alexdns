# This is inspired by the code in DNSChef: http://thesprawl.org/projects/dnschef
#
#
#
#

import syslog
import socketserver
import socket
import sys
import struct
import time

from dnslib import *

from .common import dispatch_request
from .common import acblogger as log


# DNSHandler Mixin. The class contains generic functions to parse DNS requests and
# calculate an appropriate response based on user parameters.
class DNSHandler(socketserver.BaseRequestHandler):
    def handle_data(self, data):
        response = ""

        try:
            # Parse data as DNS
            d = DNSRecord.parse(data)

        except Exception as e:
            log.error("invalid dns request", e=str(e))
        else:
            response = dispatch_request.dispatch_request(d)
            if response is None:
                log.warn("failed to lookup request", d=str(d))


        return response


# UDP DNS Handler for incoming requests
class UDPHandler(DNSHandler):
    def handle(self):
        (data,socket) = self.request
        response = self.handle_data(data)

        if response:
            socket.sendto(response, self.client_address)

# TCP DNS Handler for incoming requests
class TCPHandler(DNSHandler):
    def handle(self):
        data = self.request.recv(1024)

        # Remove the addition "length" parameter used in the
        # TCP DNS protocol
        data = data[2:]
        response = self.handle_data(data)

        if response:
            # Calculate and add the additional "length" parameter
            # used in TCP DNS protocol
            length = struct.pack(">H", len(response))
            self.request.sendall(length+response)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

# Initialize and start the DNS Server
def run_server(server_address, tcp=False, ipv6=False, port=53):
    log.info("alexdns is starting", server_address=server_address, tcp=tcp, ipv6=ipv6, port=port)
    try:
        if tcp:
            server = ThreadedTCPServer((server_address, port), TCPHandler)
        else:
            server = ThreadedUDPServer((server_address, port), UDPHandler)
        server.cache = {}
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        log.info("alexdns is shutting down")
        sys.exit()

