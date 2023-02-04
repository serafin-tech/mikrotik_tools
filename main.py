#!/usr/bin/env python3

import argparse
import ipaddress
import logging


def encode_unifi_43(payload: str) -> str:
    prefix = '0x0104'  # prefix to use for the option

    try:
        ip_addr = ipaddress.ip_address(payload)
        ip_addr_hex = f"{ip_addr:X}"
    except ValueError:
        logging.info('invalid ip address: %s', payload)
        raise

    return f'{prefix}{ip_addr_hex}'


def args_parser():
    parser = argparse.ArgumentParser(description='Script to generate MikroTik DHCP options')

    parser.add_argument('option',
                        choices=['unifi_43'],
                        help='option to generate')
    parser.add_argument('payload',
                        nargs='?',
                        help='payload to encode')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    params = parser.parse_args()

    if params.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    return params.option, params.payload


def main():
    option, payload = args_parser()

    if option == 'unifi_43':
        print(encode_unifi_43(payload))


if __name__ == '__main__':
    main()
