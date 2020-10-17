# -*- coding: utf-8 -*-

#  DNS Leak-Test a Kodi addon too check your DNS Settings
#  Copyright (C) 2020  Space2Walker
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import sys
import requests
import xbmcgui
import xbmcaddon
import xbmcplugin
import xbmcvfs
import urllib.parse as urlparse
from platform import system as system_name
from random import randint
from subprocess import call as system_call


def ping(host):
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    if system_name().lower() == "windows":
        system_call(command, creationflags=0x00000008)
    else:
        system_call(command)


def set_label(label):
    list_item = xbmcgui.ListItem(label=label)
    list_item.setArt({"fanart": background})
    xbmcplugin.addDirectoryItem(_handle, "", list_item, False)


def list_data(parsed_data, d_type):
    for dns_server in parsed_data:
        if dns_server["type"] == d_type:
            if dns_server["country_name"]:
                if dns_server["asn"]:
                    set_label(
                        f"{dns_server['ip']} [{dns_server['country_name']}, {dns_server['asn']}]"
                    )
                else:
                    set_label(f"{dns_server['ip']} [{dns_server['country_name']}]")
            else:
                set_label(str(dns_server["ip"]))


_handle = int(sys.argv[1])
my_path = xbmcaddon.Addon().getAddonInfo("path")
background = xbmcvfs.makeLegalFilename(my_path + "/resources/fanart.png")
paramstring = sys.argv[2][1:]
params = dict(urlparse.parse_qsl(paramstring))
get_local = xbmcaddon.Addon().getLocalizedString

if params == {}:
    xbmcplugin.setContent(_handle, "files")
    xbmcplugin.setPluginFanart(_handle, background)
    leak_id = randint(1000000, 9999999)
    for x in range(0, 10):
        ping(".".join([str(x), str(leak_id), "bash.ws"]))

    url = f"https://bash.ws/dnsleak/test/{str(leak_id)}?json"
    response = requests.get(url)
    parsed_data = json.loads(response.content)
    print(parsed_data)
    set_label(get_local(62001))
    list_data(parsed_data, "ip")
    servers = 0
    for dns_server in parsed_data:
        if dns_server["type"] == "dns":
            servers += 1
    if servers == 0:
        set_label(get_local(62002))
    else:
        if servers == 1:
            set_label(get_local(62003))
        else:
            set_label(get_local(62004))
        list_data(parsed_data, "dns")

    set_label(get_local(62005))
    for dns_server in parsed_data:
        if dns_server["type"] == "conclusion":
            if dns_server["ip"] == "DNS may be leaking.":
                set_label(get_local(62006))
            elif dns_server["ip"] == "DNS is not leaking.":
                set_label(get_local(62007))
    xbmcplugin.endOfDirectory(_handle, cacheToDisc=False)
