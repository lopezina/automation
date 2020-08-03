import json
import os
from pprint import pprint
from getpass import getpass
from netmiko import ConnectHandler
command = "sh ptp clock  | json-pretty"
password = "88newclass"
nxos1 = {
    "host": "nxos1.lasthop.io",
    "username": "pyclass",
    "password": password,
    "device_type": "cisco_nxos",
}

net_connect = ConnectHandler(**nxos1)
output = net_connect.send_command(command)
output_dict = json.loads(output)
print("Clock Offset: " + output_dict["offset-from-master"])
