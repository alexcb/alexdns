from dnslib import QR

import handlers.block_daisy
import handlers.fake_a
import handlers.proxy
import handlers.docker
import time

import common.acblogger as log

thehandlers = [
    handlers.block_daisy.block_daisy,
    handlers.fake_a.fake_a,
    handlers.docker.docker,
    handlers.proxy.proxy,
    ]

max_cache_time = 60

cache = {}
def dispatch_request(request):
    assert QR[request.header.qr] == "QUERY"
    key = (str(request.q.qname), str(request.q.qtype))
    log.info("searching", key=key, request_query=request.q)
    if key in cache:
        age = time.time() - cache[key]['t']
        if age < max_cache_time:
            reply = cache[key]['res']
            reply.header.id = request.header.id
            return reply.pack()

    for handler in thehandlers:
        done, request = handler(request)
        if done:
            if request:
                rcode = request.header.get_rcode()
                if rcode == 0:
                    cache[key] = {
                        't': time.time(),
                        'res': request,
                        }
                return request.pack()
            return None
    return None
