import sys
import uuid
import os
import re
import json


def write_settings(data):
    with open('/etc/imm/network.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


def write_system_config_file(text, destination):
    #generate unique filename for store in /tmp and sudo copying to destination
    filename = "/tmp/%s.imm" % uuid.uuid4()
    with open(filename, 'w') as f:
        f.write(text)

    os.system("sudo mv %s %s" % (filename, destination))
    os.system("rm %s" % filename)


def check_ip(ip):
    if re.match(r'^\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b$', ip):
        return True
    else:
        return False


def print_info():
    print '**********'
    print 'Example DHCP:'
    print 'python script_network.py dhcp'
    print 'Example STATIC:'
    print 'python script_network.py static 192.168.1.10 255.255.255.0 192.168.88.1.1 8.8.8.8'
    print '**********'


if __name__ == "__main__":
    """
    argv1 - dhcp / static
    argv2 - ip (static only)
    argv3 - mask (static only)
    argv4 - gateway (static only)
    argv5 - dns (static only)
    """

    json_data = {
        'dhcp': False,
        'static': {
            'ip': '',
            'netmask': '',
            'gateway': '',
            'dns': ''
        }
    }

    data = '# This file describes the network interfaces available on your system\n'\
        '# and how to activate them. For more information, see interfaces(5).\n'\
        '\n'\
        '# The loopback network interface\n'\
        'auto lo\n'\
        'iface lo inet loopback\n'\
        '\n'\
        '# The primary network interface\n'\
        '\n'\
        'auto eth0\n'

    # DHCP
    if len(sys.argv) == 2:
        type = sys.argv[1].upper()

        if type != 'DHCP':
            print 'Unknown argument {}, terminating...'.format(type)
            print_info()
            sys.exit(1)

        data = data + 'iface eth0 inet dhcp'
        json_data['dhcp'] = True

        write_settings(json_data)
        write_system_config_file(data, '/etc/network/interfaces')

        #with open('/home/imm/test_network.json', 'w') as f:
        #    f.write(data)

    # STATIC
    elif len(sys.argv) == 6:
        type = sys.argv[1].upper()

        if type != 'STATIC':
            print 'Unknown argument {}, terminating...'.format(type)
            print_info()
            sys.exit(1)

        ip = sys.argv[2]
        netmask = sys.argv[3]
        gateway = sys.argv[4]
        dns = sys.argv[5]

        if check_ip(ip) and check_ip(netmask) and check_ip(gateway) and check_ip(dns):
            data = data + 'iface eth0 inet static\n'\
                '    address ' + ip + '\n'\
                '    netmask ' + netmask + '\n'\
                '    gateway ' + gateway + '\n'\
                '    dns-nameservers ' + dns

            json_data['static']['ip'] = ip
            json_data['static']['netmask'] = netmask
            json_data['static']['gateway'] = gateway
            json_data['static']['dns'] = dns

            write_settings(json_data)
            write_system_config_file(data, '/etc/network/interfaces')

            #with open('/home/imm/test_network.json', 'w') as f:
            #    f.write(data)
        else:
            print 'Bad format of input arguments, terminating...'
            print_info()
            sys.exit(1)

    else:
        print 'Bad count of input arguments, terminating...'
        print_info()
        sys.exit(1)

    print 'New network settings is OK. Please, make restart...'
