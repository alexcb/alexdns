from dnslib import * #TODO

from alexdns.common.chomp_dot import chomp_dot
import alexdns.common.acblogger as log

# Obtain a response from a real DNS server.
def proxyrequest(request, host, port="53", protocol="udp"):
    ipv6 = False #TODO this should be figured out by the host
    if ipv6:
        if protocol == "udp":
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        elif protocol == "tcp":
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            assert 0
    else:
        if protocol == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            assert 0

    sock.settimeout(3.0)

    # Send the proxy request to a randomly chosen DNS server

    if protocol == "udp":
        sock.sendto(request, (host, int(port)))
        reply = sock.recv(1024)
        sock.close()

    elif protocol == "tcp":
        sock.connect((host, int(port)))

        # Add length for the TCP request
        length = binascii.unhexlify("%04x" % len(request))
        sock.sendall(length+request)

        # Strip length from the response
        reply = sock.recv(1024)
        reply = reply[2:]

        sock.close()
    else:
        raise ValueError(protocol)

    return reply

def get_nameservers(qname):
    nameservers = (
        ('.internal.mycompany.com', ['1.2.3.4'       ] ),
        ('google.com',              ['8.8.8.8'       ] ),
        ('',                        ['8.8.8.8'       ] ),
        )
    for suffix, nameserver in nameservers:
        if qname.endswith(suffix):
            return nameserver

def proxy(request):
    qname = chomp_dot(str(request.q.qname))
    qtype = QTYPE[request.q.qtype]
    raw_data = request.pack()
    nameservers = get_nameservers(qname)
    log.info("proxying request", request=request, nameservers=nameservers)
    nameserver_tuple = random.choice(nameservers).split('#')
    try:
        response = DNSRecord.parse(proxyrequest(raw_data,*nameserver_tuple))
    except Exception as e:
        log.error("proxying request failed", request=request, error=e)
        response = DNSRecord(DNSHeader(id=request.header.id, bitmap=request.header.bitmap, qr=1, ra=1, rcode=2), q=request.q)
    return True, response
