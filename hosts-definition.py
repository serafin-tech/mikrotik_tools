#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import ipaddress
import logging
from pprint import pformat
from typing import List

import macaddress
import openpyxl

DEFAULT_WORKSHEET_NAME = 'hosts-definition'
OUTPUT_TYPES = ['dns', 'dhcp']
HOSTS_DEFINITION_HEADERS = ["hostname", "domain", "ip-address", "mac-address"]


@dataclass
class HostDefinition:
    hostname: str
    domain: str
    ip_address: ipaddress.IPv4Address = None
    mac_address: macaddress.HWAddress = None


def args_parser():
    parser = argparse.ArgumentParser(description='Script to generate hosts definition for Mikrotik router')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='talkative mode')

    parser.add_argument('-f', '--file',
                        action='store',
                        required=True,
                        help='xlsx file with hosts definition')

    parser.add_argument('-o', '--output',
                        action='store',
                        help='output file')

    parser.add_argument('-t', '--output-type',
                        action='store',
                        choices=OUTPUT_TYPES,
                        required=True,
                        help=f"type of output, to be selected from {OUTPUT_TYPES}")

    params = parser.parse_args()

    return params


def logging_setup(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def read_hosts_definition_file(input_file_name: str) -> List[HostDefinition]:
    ret_definition = []

    workbook = openpyxl.load_workbook(filename=input_file_name, read_only=True)
    worksheet = workbook[DEFAULT_WORKSHEET_NAME]

    table_start_row = 2
    table_end_row = worksheet.max_row
    table_start_column = 1
    table_end_column = worksheet.max_column

    for row in worksheet.iter_rows(min_row=table_start_row,
                                   max_row=table_end_row,
                                   min_col=table_start_column,
                                   max_col=table_end_column):
        hd = HostDefinition(hostname=row[0].value,
                            domain=row[1].value,
                            ip_address=row[2].value,
                            mac_address=row[3].value)
        ret_definition.append(hd)

    workbook.close()

    logging.debug("row: %s", pformat(ret_definition))

    return ret_definition


def generate_dns_output(definition, output_file: str = None) -> None:

    for item in definition:
        line = f"add address={item.ip_address} name={item.hostname}.{item.domain}"
        print(line)
    pass


def generate_dhcp_output(definition, output_file: str = None) -> None:
    pass


def main():
    params = args_parser()

    logging_setup(params.verbose)

    logging.debug(params)

    definition = read_hosts_definition_file(params.file)

    if params.output_type == 'dns':
        generate_dns_output(definition)
    elif params.output_type == 'dhcp':
        generate_dhcp_output(definition)


if __name__ == '__main__':
    main()
