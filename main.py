# -*- coding: utf-8 -*-

import json
import requests
import xbmcgui
import xbmcplugin

from platform import system as system_name
from random import randint
from subprocess import call as system_call

try:
    import urllib2 as urllib
    from urllib2 import urlparse
except ImportError:
    import urllib.request as urllib
    import urllib.parse as urlparse

_url = sys.argv[0]

_handle = int(sys.argv[1])

def ping(host):
    param = '-n' if system_name().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    if system_name().lower()=='windows':
        retcode = system_call(command, creationflags=0x00000008)
        return retcode == 0
    else:
        retcode = system_call(command)

def get_url(_url, **kwargs):
   return '{0}?{1}'.format(_url, urllib.urlencode(kwargs))

def set_label(label):
    list_item = xbmcgui.ListItem(label=label)
    list_item.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

def list_data(parsed_data, d_type):
    for dns_server in parsed_data:
        if dns_server['type'] == d_type:
            if dns_server['country_name']:
                if dns_server['asn']:
                    set_label(dns_server['ip']
                                + " [" + dns_server['country_name']
                                + ", " + dns_server['asn']
                                + "]")

                else:
                    set_label(dns_server['ip']
                                + " [" + dns_server['country_name']
                                +"]")

            else:
                set_label(str(dns_server['ip']))

if __name__ == '__main__':

    paramstring = sys.argv[2][1:]
    params = dict(urlparse.parse_qsl(paramstring))

    #################################
    #           1st Start           #
    #################################
    if params == {}:
        xbmcplugin.setPluginCategory(_handle, 'category')
        xbmcplugin.setContent(_handle, 'videos')

        leak_id = randint(1000000,9999999)
        for x in range (0, 10):
            ping('.'.join([str(x),str(leak_id),"bash.ws"]))

        url = "https://bash.ws/dnsleak/test/" + str(leak_id) + "?json"
        response = requests.get(url)
        parsed_data = json.loads(response.content)

        set_label('Your IP:')
        list_data(parsed_data, "ip")

        servers = 0

        for dns_server in parsed_data:
            if dns_server['type'] == "dns":
                servers = servers + 1

        if servers == 0:
            set_label("No DNS servers found")

        else:
            set_label("You use "+str(servers)+" DNS servers:")
            list_data(parsed_data, "dns")

        set_label("Conclusion:")

        for dns_server in parsed_data:
            if dns_server['type'] == "conclusion":
                if dns_server['ip']:
                    set_label(str(dns_server['ip']))

        xbmcplugin.endOfDirectory(_handle)
        quit()

    #################################
    #             error             #
    #################################
    # If the provided paramstring does not contain a supported action
    # we raise an exception. This helps to catch coding errors,
    # e.g. typos in action names.
    raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    quit()
