from common.chomp_dot import chomp_dot #TODO i dont like this import
import common.acblogger as log

blacklist = [
    'daisy.ubuntu.com',
    ]

def block_daisy(d):
    qname = chomp_dot(str(d.q.qname))
    for x in blacklist:
        if qname.endswith(x):
            log.info("blocking host", host=qname)
            return True, None
    return False, d
