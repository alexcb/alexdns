from dnslib import * #TODO
from common.chomp_dot import chomp_dot #TODO i dont like this import
from common.is_ip import is_ipv4 #TODO i dont like this import
from common.resolver import query_A
import common.acblogger as log

overrides = {
    'music.': '192.168.0.10',
    'lidar.': '10.124.56.77',
    #'monkey.': 'mofo.ca', # can also redirect as a CNAME
    }
assert(all(x.endswith('.') for x in overrides))


def fake_a(d):
    qtype = QTYPE[d.q.qtype]
    log.info("got qtype", host=qtype)
    if qtype != 'A':
        return False, d

    qname = str(d.q.qname)
    log.info("got qname", host=qname)

    if qname not in overrides:
        log.info("not overridding dns", host=qname)
        return False, d

    fake_record = overrides[qname]
    log.info("overridding dns", host=qname, override=fake_record)

    response = DNSRecord(DNSHeader(id=d.header.id, bitmap=d.header.bitmap, qr=1, aa=1, ra=1), q=d.q)
    if is_ipv4(fake_record):
        # Oct 23 11:07:39 sunfish MainProcess[15881]: {"msg": "", "blah": "('music.', 1, 192.168.0.10)", "level": "INFO"}
        log.info("", blah=repr((qname, QTYPE.A, RDMAP['A'](fake_record))))
        response.add_answer(RR(qname, QTYPE.A, rdata=RDMAP['A'](fake_record)))
    else:
        response.add_answer(RR(qname, QTYPE.CNAME, rdata=RDMAP['CNAME'](chomp_dot(fake_record))))
        for ip in query_A(fake_record, '8.8.8.8'):
            response.add_answer(RR(qname, QTYPE.A, rdata=RDMAP['A'](ip)))
    return True, response
