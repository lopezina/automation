import os
from netmiko import ConnectHandler
from getpass import getpass


def display_output(output):
    print()
    print("#" * 80)
    print("CFG Change: ")
    print(output)
    print("#" * 80)
    print()
def display_output1(output, device):
    print()
    print("#" * 80)
    print(str(device['host']) + ": ")
    print(output)
    print("#" * 80)
    print()

if __name__ == "__main__":
    password = "88newclass"
    nxos1 = {
        "host": "nxos1.lasthop.io",
        "username": "pyclass",
        "password": password,
        "device_type": "cisco_nxos",
    }
    nxos2 = {
        "host": "nxos2.lasthop.io",
        "username": "pyclass",
        "password": password,
        "device_type": "cisco_nxos",
    }

    for device in (nxos1, nxos2):
        net_connect = ConnectHandler(**device)
        output = net_connect.send_config_from_file("vlans.txt")
        display_output1(output, device)
        net_connect.save_config()
        net_connect.disconnect()
