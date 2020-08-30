import os
import csv
import pyeapi
from getpass import getpass
from my_funcs import yaml_load_devices
from pprint import pprint
hosts_info = list()
secret=getpass()
with open('arista', 'r') as devices:
    csv_reader = csv.reader(devices, delimiter=',')
    for row in csv_reader:
        host = {
            'transport': 'https',
            'host': row[0],
            'username': 'pyclass',
            'port': '443',
            'password': secret 
        }
        #hosts_info.append(host)
        connection = pyeapi.client.connect(**host)
        device = pyeapi.client.Node(connection)
        output = device.enable("show ip route")
        routes = output[0]["result"]["vrfs"]["default"]["routes"]
        print()
        print(row[0])
        print("-" * 40)
        deviceroute=list()
        for prefix, route_dict in routes.items():
            route_type = route_dict["routeType"]
            if route_type != "connected":
                nexthop=route_dict["vias"][0]["nexthopAddr"]
                eachroute=[prefix, nexthop, route_type]
                deviceroute.append(eachroute)
            #print("{:16}{:15}{:10}".format(prefix, nexthop, route_type))
        for item in deviceroute:
            x, y, z = item
            print("{:16}{:15}{:10}".format(x, y, z))
        print("-" * 40)
print()
