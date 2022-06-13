# Copyright 2019 Belma Turkovic
# TU Delft Embedded and Networked Systems Group.
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from p4_mininet import P4Switch, P4Host, P4GrpcSwitch

# from p4runtime_switch import P4RuntimeSwitch
import random
import argparse
from time import sleep
import subprocess
import sys
import os
import psutil

parser = argparse.ArgumentParser(description="Mininet demo")
# parser.add_argument('--thrift-port', help='Thrift server port for table updates', type=int, action="store", default=9090)
parser.add_argument(
    "--num-hosts",
    help="Number of hosts to connect to switch",
    type=int,
    action="store",
    default=2,
)
parser.add_argument(
    "--p4-file", help="Path to P4 file", type=str, action="store", required=False
)

args = parser.parse_args()


def get_all_virtual_interfaces():
    try:
        return (
            subprocess.check_output(
                ["ip addr | grep s.-eth. | cut -d':' -f2 | cut -d'@' -f1"], shell=True
            )
            .decode(sys.stdout.encoding)
            .splitlines()
        )
    except subprocess.CalledProcessError as e:
        print("Cannot retrieve interfaces.")
        print(e)
        return ""


class SingleSwitchTopo(Topo):
    "Single switch connected to n (< 256) hosts."

    def __init__(self, sw_path, json_path, n, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switch = self.addSwitch(
            "s0",
            sw_path=sw_path,
            json_path=json_path,
            grpc_port=50051,
            device_id=1,
            cpu_port="255",
        )

        for h in range(0, n):
            host = self.addHost(
                "h%d" % (h + 1),
                ip="10.10.10.%d/16" % (h + 1),
                mac="00:04:00:00:00:%02x" % h,
            )
            self.addLink(host, switch)
        server = self.addHost("server", ip="10.10.3.3/16", mac="00:00:01:01:01:01")
        self.addLink(server, switch)


def main():
    num_hosts = int(args.num_hosts)
    result = os.system(
        "p4c --target bmv2 --arch v1model --p4runtime-files firmeware.p4info.txt "
        + args.p4_file
    )
    p4_file = args.p4_file.split("/")[-1]
    json_file = p4_file.split(".")[0] + ".json"

    topo = SingleSwitchTopo("simple_switch_grpc", json_file, num_hosts)
    net = Mininet(
        topo=topo, host=P4Host, switch=P4GrpcSwitch, link=TCLink, controller=None
    )
    net.start()

    interfaces = get_all_virtual_interfaces()
    for i in interfaces:
        if i != "":
            os.system("ip link set {} mtu 1600 > /dev/null".format(i))
            os.system("ethtool --offload {} rx off  tx off > /dev/null".format(i))
    net.staticArp()

    if result != 0:
        print("Error while compiling!")
        exit()

    switch_running = "simple_switch_grpc" in (p.name() for p in psutil.process_iter())
    if switch_running == False:
        print("The switch didnt start correctly! Check the path to your P4 file!!")
        exit()

    print("Starting mininet!")

    CLI(net)


if __name__ == "__main__":
    setLogLevel("info")
    main()
