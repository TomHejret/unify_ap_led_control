#!/usr/bin/env python3

# Copyright 2022 Tom Hejret.
# SPDX-License-Identifier: GNU v.3

import json
import os
import sys
from io import UnsupportedOperation
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

import requests


# fill according to your setup
username_default = '???'
pwd_default = '???'
host_default = '???'
AP_mac_default = '???'

login_url = f'https://{host_default}:8443/api/login'
led_url = f'https://{host_default}:8443/api/s/default/cmd/devmgr'
session_file = 'unifi_ssn.json'

STATE_ON = 'set-locate'		# state to enable "locate" AP blinking
STATE_OFF = 'unset-locate'

login_payload = {
    'username': username_default,
    'password': pwd_default,
    'remember': False,
    'strict': True
}


def ap_login():
    print('Login to AP')
    response = requests.post(login_url, data=json.dumps(login_payload), verify=False)
    cookies = response.cookies
    headers = response.headers
    headers['X-Csrf-Token'] = cookies.get('csrf_token')
    unify_session = {
        'headers': dict(headers),
        'cookies': cookies.get_dict()
    }
    print(response.text)
    print(unify_session)
    with open(session_file, 'w') as unifi_ssn_file:
        json.dump(unify_session, unifi_ssn_file)
    return unify_session


def led_status(AP_mac, on=True):
    unify_session = None
    if os.path.exists(session_file):
        with open(session_file, 'r') as unifi_ssn_file:
            try:
                unify_session = json.load(unifi_ssn_file)
                print('Loaded AP session')
            except UnsupportedOperation as uo:
                print(str(uo))
    if unify_session is None:
        unify_session = ap_login()

    led_payload = {
        'mac': AP_mac,
        'cmd': STATE_ON if on else STATE_OFF
    }
    response = requests.post(led_url, data=json.dumps(led_payload),
                             headers=unify_session['headers'],
                             cookies=unify_session['cookies'],
                             verify=False)
    print(response.text)
    return response.json()['meta']['rc'] == 'ok'


if __name__ == "__main__":
    parser = ArgumentParser(usage='To turn on/off locating AP LED blinking',
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            description='Run PyRock tests')
    parser.add_argument('--off', action='store_false', dest='set_state_ON')
    parser.add_argument('--mac', dest='AP_mac', help='AP MAC address',
                        default=AP_mac_default)
    options = parser.parse_args(sys.argv[1:])

    if not led_status(options.AP_mac, options.set_state_ON):
        # try again in case the credentials (tokens) from file are expired
        os.remove(session_file)
        led_status(options.AP_mac, options.set_state_ON)
