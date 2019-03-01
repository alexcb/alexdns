import dns.resolver

def query_A(dnsquery, nameservers):
    if isinstance(nameservers, basestring):
        nameservers = [nameservers]
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = nameservers
    answers = resolver.query(dnsquery, 'A')
    return [x.address for x in answers]
