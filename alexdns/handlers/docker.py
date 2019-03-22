import subprocess
import json

from dnslib import * #TODO

import alexdns.common.acblogger as log
from alexdns.common.chomp_dot import chomp_dot #TODO i dont like this import

def split_docker_name(x):
    x = x.split('.')
    if len(x) == 1:
        return x[0], None
    if len(x) == 2:
        return x[0], x[1]
    raise ValueError(x)

def get_docker_ip(container_name):
    container_name, container_network = split_docker_name(container_name)
    s = subprocess.check_output(['/usr/bin/docker', 'inspect', container_name], encoding='ascii')
    x = json.loads(s)
    for network_name, vals in x[0]['NetworkSettings']['Networks'].items():
        if network_name == container_network or container_network is None:
            return vals['IPAddress']
    raise RuntimeError('failed to get docker ip')

def docker(d):
    qname = chomp_dot(str(d.q.qname))

    # optimization to avoid shelling out
    if qname.count('.') > 1:
        return False, d
    if qname.count('.') == 1 and qname.endswith('.com'):
        return False, d

    try:
        ip = get_docker_ip(qname)
    except Exception as e:
        log.error("failed to get docker ip", e=e, qname=qname)
        return False, d

    log.info("resolved docker hostname", host=d, override=ip)
    response = DNSRecord(DNSHeader(id=d.header.id, bitmap=d.header.bitmap, qr=1, aa=1, ra=1), q=d.q)
    response.add_answer(RR(qname, QTYPE.A, rdata=RDMAP['A'](ip)))
    return True, response
