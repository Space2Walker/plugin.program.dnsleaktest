import json
from platform import system as system_name
from random import randint
from subprocess import call as system_call
import requests


def perform_ping():
    """
    builds the identification and performs the series of pings
    to <idenification>.bash.ws too trigger the DNS requests

    :return: identification
    """
    identification = str(randint(1000000, 9999999))
    for x in range(0, 10):
        ping_command(".".join([str(x), identification, "bash.ws"]))
    return identification


def get_response(identification):
    """
    Gets the response data from the bash.ws api

    :param str identification: The ID
    :return:
    """
    url = f"https://bash.ws/dnsleak/test/{identification}?json"
    response = requests.get(url)
    parsed_data = json.loads(response.content)
    return parsed_data


def ping_command(host):
    """
    Perform a Platform specific PING command

    :param str host: The host to Ping
    """
    param = "-n" if system_name().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    if system_name().lower() == "windows":
        system_call(command, creationflags=0x00000008)
    else:
        system_call(command)
