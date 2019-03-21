# -*- coding: utf-8 -*-

import json
import requests
import xbmcgui
import xbmcplugin

from platform import system as system_name
from random import randint
from subprocess import call as system_call
from urlparse import parse_qsl
from urllib import urlencode

_url = sys.argv[0]

_handle = int(sys.argv[1])

def ping(host):
    param = '-n' if system_name().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    retcode = system_call(command, creationflags=0x00000008)
    return retcode == 0

def get_url(_url, **kwargs):
   return '{0}?{1}'.format(_url, urlencode(kwargs))

def set_label(label):
    list_item = xbmcgui.ListItem(label=label)
    list_item.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

if __name__ == '__main__':

    paramstring = sys.argv[2][1:]
    params = dict(parse_qsl(paramstring))

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

        for dns_server in parsed_data:
            if dns_server['type'] == "ip":
                if dns_server['country_name']:
                    if dns_server['asn']:
                        set_label(dns_server['ip']+" ["+dns_server['country_name']+", "+dns_server['asn']+"]")

                    else:
                        set_label(dns_server['ip']+" ["+dns_server['country_name']+"]")
 
                else:
                    set_label(str(dns_server['ip']))

        servers = 0

        for dns_server in parsed_data:
            if dns_server['type'] == "dns":
                servers = servers + 1
        
        if servers == 0:
            set_label("No DNS servers found")

        else:
            set_label("You use "+str(servers)+" DNS servers:")

            for dns_server in parsed_data:
                if dns_server['type'] == "dns":
                    if dns_server['country_name']:
                        if dns_server['asn']:
                            set_label(dns_server['ip']+" ["+dns_server['country_name']+", "+dns_server['asn']+"]")

                        else:
                            set_label(dns_server['ip']+" ["+dns_server['country_name']+"]")

                    else:
                        set_label(str(dns_server['ip']))
                        
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
