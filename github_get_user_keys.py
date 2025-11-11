#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring,missing-class-docstring
"""
get GitHub user ssh-keys and generate Mikrotik commands for adding them to the router.
"""
import argparse
import json

from typing import NamedTuple
from string import Template
from urllib.request import urlopen, Request
from urllib.error import HTTPError

GITHUB_API_BASE_URL = "https://api.github.com/users"

MT_ADD_KEY_COMMAND_TEMPLATE = Template(
    "/user/ssh-keys/add user=${user} key=\"${key}\"")


class UsersTuple(NamedTuple):
    github_user: str
    mikrotik_user: str


def read_keys_from_gh(user: str) -> list[str]:
    github_api_url = f"{GITHUB_API_BASE_URL}/{user}/keys"

    try:
        with urlopen(Request(url=github_api_url,
                             data=None,
                             headers={
                                 'Accept': 'application/vnd.github+json',
                                 'X-GitHub-Api-Version': '2022-11-28'
                             })) as response:
            keys = json.loads(response.read())
            return [key['key'] for key in keys]

    except (IOError, HTTPError) as error:
        raise ValueError(
            f"Invalid HTTP response from {github_api_url}") from error


def get_users_from_args() -> UsersTuple:
    parser = argparse.ArgumentParser()

    parser.add_argument('github_user',
                        help='GitHub user to read SSH-keys for')

    parser.add_argument('mikrotik_user',
                        help='Mikrotik user to add SSH-keys for')

    parsed_args = parser.parse_args()

    return UsersTuple(parsed_args.github_user, parsed_args.mikrotik_user)


def main():
    users_tuple = get_users_from_args()

    keys = read_keys_from_gh(users_tuple.github_user)

    print("# beginning of the Mikrotik commands")

    for key in keys:
        print(MT_ADD_KEY_COMMAND_TEMPLATE.substitute(
            user=users_tuple.mikrotik_user, key=key))

    print("# end of the Mikrotik commands")


if __name__ == "__main__":
    main()
