import csv
import json
from netmiko import ConnectHandler
import time
import concurrent.futures
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from password_protect import (
p_file_path, key_file_path, store_mgmt_password, get_mgmt_password, generate_key_file)
from os.path import exists
# check for symmetric key.
# if does not exists create one.
if not exists(key_file_path):
    generate_key_file()
 
# check if p.txt is present or not, if not prompt for one.
# then encrypt the password and save as p.txt.
if not exists(p_file_path):
    store_mgmt_password()



starting_time = time.perf_counter()
fork = 5


hosts_info = list()

with open('nexus', 'r') as devices:
    csv_reader = csv.reader(devices, delimiter=',')
    for row in csv_reader:
        host = {
            #'device_type': row[1],
            'device_type': 'cisco_nxos',
            'ip': row[0],
            'username': 'pyclass',
            'password': get_mgmt_password(),
            'secret': 'cisco'
        }
        hosts_info.append(host)


def open_connection(host):
    try:
        connection = ConnectHandler(**host)
        #print('Connection Established to Host:', host['ip'])
        connection.enable()
        sendcommand = connection.send_command('sh ver', use_textfsm=True)
        #return sendcommand
        return "{:20}{:5}{}".format(host['ip'], "is", sendcommand[0]['platform'])

    except NetMikoTimeoutException:
        print(host['ip'], 'Device not reachable.')
    except AuthenticationException:
        print('Authentication Failure on: ', host['ip'])
    except SSHException:
        print('Make sure SSH is enabled on device: ', host['ip'])


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=fork) as executor:
        results = executor.map(open_connection, hosts_info)
        print('\n')
        for result in results:
            if result:
                print(result)

    finish = time.perf_counter()
    print('\n')
    print('Script runtime:', finish - starting_time, 'Secs')


