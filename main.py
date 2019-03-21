# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 02.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

# https://bash.ws/dnsleak

import os
import subprocess
import json
from random import randint
from platform import system as system_name
from subprocess import call as system_call
from random import randint
from urlparse import parse_qsl
from urllib import urlencode
import sys
import xbmcgui
import xbmc
import xbmcplugin

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def ping(host):
    fn = open(os.devnull, 'w')
    param = '-n' if system_name().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    retcode = system_call(command, stdout=fn, stderr=subprocess.STDOUT)
    fn.close()
    return retcode == 0

def get_url(_url, **kwargs):
   return '{0}?{1}'.format(_url, urlencode(kwargs))

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]

# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

if __name__ == '__main__':

    # We use string slicing to trim the leading '?'
    # from the plugin call paramstring
    paramstring = sys.argv[2][1:]

    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    #xbmc.log(str(params),level=xbmc.LOGNOTICE)

    # Check the parameters passed to the plugin give new and restart
    # quit() is needed at the end of each if

    #################################
    #           1st Start           #
    #################################
    if params == {}:
        xbmcplugin.setPluginCategory(_handle, 'category')
        xbmcplugin.setContent(_handle, 'videos')

        leak_id = randint(1000000,9999999)
        for x in range (0, 10):
            ping('.'.join([str(x),str(leak_id),"bash.ws"]))
        
        response = urlopen("https://bash.ws/dnsleak/test/"+str(leak_id)+"?json")
        data = response.read().decode("utf-8")
        parsed_data = json.loads(data)
        
        list_item = xbmcgui.ListItem(label='Your IP:') 
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

        xbmc.log("",level=xbmc.LOGNOTICE)
        for dns_server in parsed_data:
            if dns_server['type'] == "ip":
                if dns_server['country_name']:
                    if dns_server['asn']:
                        out = dns_server['ip']+" ["+dns_server['country_name']+", "+dns_server['asn']+"]"
                        list_item = xbmcgui.ListItem(label=out) 
                        list_item.setProperty('IsPlayable', 'false')
                        xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

                        xbmc.log(str(out),level=xbmc.LOGNOTICE)
                    else:
                        out = dns_server['ip']+" ["+dns_server['country_name']+"]"
                        list_item = xbmcgui.ListItem(label=out) 
                        list_item.setProperty('IsPlayable', 'false')
                        xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

                        xbmc.log(str(out),level=xbmc.LOGNOTICE)
                else:
                    list_item = xbmcgui.ListItem(label=str(dns_server['ip']))
                    list_item.setProperty('IsPlayable', 'false')
                    xbmcplugin.addDirectoryItem(_handle, '', list_item, False)
                    xbmc.log(str(dns_server['ip']),level=xbmc.LOGNOTICE)
        
        servers = 0

        for dns_server in parsed_data:
            if dns_server['type'] == "dns":
                servers = servers + 1
        
        if servers == 0:
            list_item = xbmcgui.ListItem(label="No DNS servers found")
            list_item.setProperty('IsPlayable', 'false')
            xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

        else:
            list_item = xbmcgui.ListItem(label="You use "+str(servers)+" DNS servers:")
            list_item.setProperty('IsPlayable', 'false')
            xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

            for dns_server in parsed_data:
                if dns_server['type'] == "dns":
                    if dns_server['country_name']:
                        if dns_server['asn']:
                            out = dns_server['ip']+" ["+dns_server['country_name']+", "+dns_server['asn']+"]"
                            list_item = xbmcgui.ListItem(label=out)
                            list_item.setProperty('IsPlayable', 'false')
                            xbmcplugin.addDirectoryItem(_handle, '', list_item, False)
                        else:
                            out = dns_server['ip']+" ["+dns_server['country_name']+"]"
                            list_item = xbmcgui.ListItem(label=out)
                            list_item.setProperty('IsPlayable', 'false')
                            xbmcplugin.addDirectoryItem(_handle, '', list_item, False)
                    else:
                        list_item = xbmcgui.ListItem(label=str(dns_server['ip']))
                        list_item.setProperty('IsPlayable', 'false')
                        xbmcplugin.addDirectoryItem(_handle, '', list_item, False)
                        
            
        list_item = xbmcgui.ListItem(label="Conclusion:")
        list_item.setProperty('IsPlayable', 'false')
        xbmcplugin.addDirectoryItem(_handle, '', list_item, False)

        for dns_server in parsed_data:
            if dns_server['type'] == "conclusion":
                if dns_server['ip']:
                    list_item = xbmcgui.ListItem(label=str(dns_server['ip']))
                    list_item.setProperty('IsPlayable', 'false')
                    xbmcplugin.addDirectoryItem(_handle, '', list_item, False)
      
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
