#!/usr/bin/env python3

# Script to update a domain via python-script

# 2025-12-31 doctore74 <doc(at)snowheaven.de>

# https://github.com/inwx/python-client/
# https://github.com/inwx/python-client/issues/9

# How to use
# 1. clone the repo - git clone https://github.com/inwx/python-client/
# 2. copy this file to the root directory of the cloned repo
# 3. chmod +x inwx_update_domain.py
# 4. enter INWX credentials, your domain and the dns entry id which you want to update
# 5. start file ./inwx_update_domain.py
#
# - you can copy the file to update several domains
# - you can use this file as cronjob
#
# Cronjob example
# */5 * * * * /root/python-client/inwx_update_domain.py > /var/log/inwx_update_domain.log 2>&1
# Example for Checkmk monitoring
# */5 * * * * mk-job inwx_update_domain /root/python-client/inwx_update_domain.py > /var/log/inwx_update_domain.log 2>&1

from INWX.Domrobot import ApiClient, ApiType
import urllib.request

# INWX credentials
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
domain = 'YOUR_DOMAIN'

# Find the SAVE button for the dns entry in your INWX website and copy the ID (xxxxxxxxx)
# javascript:saveRecord("XXXXXXXXXX","/en/nameserver2/updaterecordajax/id/1689759058","DNS_REC")
DNS_RECORD_ID = 1689759058  # your DNS record ID

def get_public_ip():
    # with urllib.request.urlopen("https://api.ipify.org") as response: # IPv4 only
    with urllib.request.urlopen("https://api64.ipify.org/") as response:
        return response.read().decode().strip()


def main():
    public_ip = get_public_ip()
    print(f"Detected public IP: {public_ip}")

    api_client = ApiClient(
        api_url=ApiClient.API_LIVE_URL,
        api_type=ApiType.JSON_RPC,
        debug_mode=True
    )

    login_result = api_client.login(username, password)

    if login_result['code'] != 1000:
        raise Exception(
            f"API login error. Code: {login_result['code']}  Message: {login_result['msg']}"
        )

    method_params = {
        'id': DNS_RECORD_ID,
        'content': public_ip,   # set your public ip
        # 'content': '1.2.3.4', # set a specific ip
    }

    update_result = api_client.call_api(
        api_method='nameserver.updateRecord',
        method_params=method_params
    )

    if update_result['code'] == 1000:
        print('Record updated successfully')
    else:
        raise Exception(
            f"API error while updating the record. "
            f"Code: {update_result['code']}  Message: {update_result['msg']}"
        )

    api_client.logout()


if __name__ == "__main__":
    main()
