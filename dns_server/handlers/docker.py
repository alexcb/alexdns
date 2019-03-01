import subprocess
import json

from dnslib import * #TODO

import common.acblogger as log
from common.chomp_dot import chomp_dot #TODO i dont like this import

def get_docker_ip(container_name):
    s = subprocess.check_output(['/usr/bin/docker', 'inspect', container_name])
    x = json.loads(s)
    return x[0]['NetworkSettings']['Networks'].values()[0]['IPAddress']


def docker(d):
    qname = chomp_dot(str(d.q.qname))

    # optimization to avoid shelling out
    if '.' in qname:
        return False, d

    try:
        ip = get_docker_ip(qname)
    except:
        return False, d

    log.info("resolved docker hostname", host=d, override=ip)
    response = DNSRecord(DNSHeader(id=d.header.id, bitmap=d.header.bitmap, qr=1, aa=1, ra=1), q=d.q)
    response.add_answer(RR(qname, QTYPE.A, rdata=RDMAP['A'](ip)))
    return True, response
