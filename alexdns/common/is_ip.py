def is_ipv4(s):
    ip = s.split('.')
    if len(ip) != 4:
        return False
    for x in ip:
        try:
            i = int(x)
        except ValueError:
            return False
        if i < 0 or i > 255:
            return False
    return True
