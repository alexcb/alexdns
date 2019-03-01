import argparse
from alex_dns import run_server


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--port', default=53, type=int, help='port to listen on (default: %(default)s)')
    return parser

def get_args():
    return get_parser().parse_args()

if __name__ == "__main__":
    args = get_args()
    run_server(server_address="0.0.0.0", tcp=False, ipv6=False, port=args.port)
