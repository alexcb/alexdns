import logging
import logging.handlers
import json

log = logging.getLogger("structlog")

log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

# options are documented in https://docs.python.org/2/library/logging.html#logrecord-attributes
formatter = logging.Formatter('%(processName)s[%(process)d]: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

_allowed_types = [
    str,
    int,
    float,
    bool,
    ]
def convert_val(x):
    for allowed in _allowed_types:
        if isinstance(x, allowed):
            return x
    return str(x)

def format_msg(msg, level, **kwargs):
    x = {k:convert_val(v) for k, v in kwargs.items()}
    x['msg'] = msg
    x['level'] = level
    return json.dumps(x)

def debug(msg, **kwargs):
    log.debug(format_msg(msg, 'DEBUG', **kwargs))

def info(msg, **kwargs):
    log.info(format_msg(msg, 'INFO', **kwargs))

def warn(msg, **kwargs):
    log.warn(format_msg(msg, 'WARN', **kwargs))

def error(msg, **kwargs):
    log.error(format_msg(msg, 'ERROR', **kwargs))

