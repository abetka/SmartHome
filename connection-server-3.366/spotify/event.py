import sys
from datetime import datetime
import socket
from struct import pack, unpack
import json
from threading import Thread


PATH_CONFIG = "/etc/imm/spotify.json"
PATH_NETWORK = "/etc/imm/network_settings.json"
PATH_LOG = "/opt/imm/imm_server/log/spotify.log"


log_enabled = True
thread_msg = ""


def readNetworkSettings():
    try:
        with open(PATH_NETWORK, 'r') as f:
            return json.load(f)
    except:
        return {}


def readConfig():
    try:
        with open(PATH_CONFIG, 'r') as f:
            return json.load(f)
    except:
        return {}


def writeConfig(data):
    try:
        with open(PATH_CONFIG, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        pass


def writeToLogFile(msg, time=True):
    if log_enabled:
        try:
            with open(PATH_LOG, 'a') as f:
                if time:
                    now = datetime.now()
                    msg = "%s: %s\r\n" % (now.strftime("%d.%m.%Y - %H:%M:%S"), msg)
                f.write(msg)
        except:
            pass


def sendPacket(server_ip, player_ip, fce):

    def writeToLogFileThread(msg):
        global thread_msg
        try:
            now = datetime.now()
            thread_msg += "%s: %s\r\n" % (now.strftime("%d.%m.%Y - %H:%M:%S"), msg)
        except:
            pass

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.settimeout(2)
        my_socket.connect((player_ip, 61695))
        output_data = [0xFF, 0xFB, 0xFB, 0xCC]
        if fce.lower() == "start":
            output_data += [0x0F]
            tmp = " >> Spotify"
            output_data += [ord(x) for x in tmp] + [0] * (13 - len(tmp))
            tmp = server_ip.split(".")
            output_data += [int(x) for x in tmp]
            output_data += [0xC3, 0x50]
            tmp = "spotify"
            output_data += [ord(x) for x in tmp] + [0] * (70 - len(tmp))
        elif fce.lower() == "stop":
            output_data += [0x04, 0x00]
        output_data = pack("{}B".format(len(output_data)), *output_data)
        my_socket.send(output_data)
        my_socket.close()
        writeToLogFileThread("Send \"%s\" to device \"%s\"" % (fce, player_ip))
    except:
        writeToLogFileThread("Cannot send \"%s\" to device \"%s\"!" % (fce, player_ip))


def runEvent(msg):
    if msg.lower() in ["start", "stop"]:
        config = readConfig()
        network_settings = readNetworkSettings()
        if config and config.get("player_ip", []) and network_settings.get("ip", ""):
            threads = []
            for ip in config["player_ip"]:
                if not ip:
                    continue
                threads.append(Thread(target=sendPacket, args=(network_settings["ip"], ip, msg, )))
            for fce in threads:
                fce.start()
            for fce in threads:
                fce.join()
            writeToLogFile(thread_msg, False)
        else:
            writeToLogFile("Cannot open config file!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        writeToLogFile("Bad count of input arguments, terminating...")
        sys.exit(1)

    writeToLogFile("Run event script...")
    runEvent(sys.argv[1])
    writeToLogFile("All done, terminating...")
