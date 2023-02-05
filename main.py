#!/usr/bin/env python3

import argparse
import ipaddress
import logging
import pprint
from typing import List


def encode_unifi_43(payload: str) -> str:
    prefix = '0x0104'  # prefix to use for the option

    try:
        ip_addr = ipaddress.ip_address(payload)
        ip_addr_hex = f"{ip_addr:X}"
    except ValueError:
        logging.info('invalid ip address: %s', payload)
        raise

    return f'{prefix}{ip_addr_hex}'


def encode_classless_routes(payload: List[str]) -> str:
    prefix = '0x0'  # prefix to use for the option
    ret = []

    for route_spec in payload:
        logging.debug("processing %s...", route_spec)
        network, gateway = route_spec.split(' ')
        logging.debug("network: %s, gateway: %s", network, gateway)

        try:
            network_addr = ipaddress.ip_network(network)
            gateway_addr = ipaddress.ip_address(gateway)

            if network_addr.prefixlen > 24:
                network_addr_hex_length = 8
            elif 16 < network_addr.prefixlen <= 24:
                network_addr_hex_length = 6
            elif 8 < network_addr.prefixlen <= 16:
                network_addr_hex_length = 4
            elif 0 < network_addr.prefixlen <= 8:
                network_addr_hex_length = 2
            else:
                network_addr_hex_length = 0

            network_addr_hex = f'{network_addr.network_address:X}'[:network_addr_hex_length]

            logging.debug("network_address: %s, prefixlen: %s, network_addr_hex: %s",
                          network_addr.network_address, network_addr.prefixlen, network_addr_hex)

            ret.append(f'{network_addr.prefixlen:X}{network_addr_hex}{gateway_addr:X}')

        except ValueError:
            logging.info('invalid route spec: %s', route_spec)
            raise

    return f"{prefix}{''.join(ret)}"


def args_parser():
    parser = argparse.ArgumentParser(description='Script to generate MikroTik DHCP options')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    subparsers = parser.add_subparsers(dest='option')

    unifi_43 = subparsers.add_parser('unifi_43', help='Option 43 for Unifi Controller address')
    unifi_43.add_argument('address',
                          help='address to encode')

    classless_routes = subparsers.add_parser('classless_routes', help='Option 121 for classless static routes')
    classless_routes.add_argument('route_spec',
                                  nargs='+',
                                  help='route specification to encode in format "a.b.c.d/e 1.2.3.4", '
                                       'first spec MUST be for default route in format "0.0.0.0/0 1.2.3.4"')

    params = parser.parse_args()

    return params


def logging_setup(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def main():
    params = args_parser()

    logging_setup(params.verbose)

    if params.option == 'unifi_43':
        logging.debug(pprint.pformat(params))
        logging.info("encoded value: %s", encode_unifi_43(params.address))

        # /ip dhcp-server option add code=43 name=unifi-controller-addr value=0x0104C0A80001
    elif params.option == 'classless_routes':
        logging.debug(pprint.pformat(params))
        logging.info("encoded value: %s", encode_classless_routes(params.route_spec))

        # /ip dhcp-server option add code=121 name=classless-static-route-option value=0x00C0A8000118C0A800C0A80001


if __name__ == '__main__':
    main()
