# Simple-P4runtime-Controller

## Mininet with simple_switch_grpc
The scripts starts a very simple Mininet topo with just one switch, n hosts and 1 server host. Additionally, it compiles the supplied P4 file to generate both the JSON as well as P4Info file (used by the controller)
```bash 
usage: run_mininet.py [-h] [--num-hosts NUM_HOSTS] [--p4-file P4_FILE]

Mininet demo

optional arguments:
  -h, --help            show this help message and exit
  --num-hosts NUM_HOSTS
                        Number of hosts to connect to switch
  --p4-file P4_FILE     Path to P4 file
```
## P4Runtime controller
Dummy P4Runtime controller with packet-in/packet-out functionality. 

```bash 
usage: controller.py [-h] [--p4info P4INFO] [--bmv2-json BMV2_JSON]

P4Runtime Controller

optional arguments:
  -h, --help            show this help message and exit
  --p4info P4INFO       p4info proto in text format from p4c
  --bmv2-json BMV2_JSON
                        BMv2 JSON file from p4c

```
At the start of the connection, the controller installs three rules, forwarding the packets to the CPU port. Furthermore, it listens to PacketIn messages and outputs them to port 3. 

### Packet-In messages
At the beginning of each packet_in message, a special header containing the ingress port is appended—these values translate to the controller's metadata values.

```bash 
 @controller_header("packet_in")
 header packet_in_t {
    bit<16> ingress_port;
 }
 ```

### Packet-Out messages
At the beginning of each packet Out message, a special header containing the egress port is appended. This value is set at the controller (as metadata in the buildPacketOut function)

```bash 
 @controller_header("packet_in")
 header packet_in_t {
     bit<16> ingress_port;
 }
 ```
## Run a test scenario

### Start Mininet (with simple_switch_grpc)
```bash 
python3 run_mininet.py --p4-file simple.p4

```
### Start the controller in a different terminal
```bash 
python3 controller.py --p4info firmeware.p4info.txt --bmv2-json simple.json
```
### Generate traffic (in Mininet)
```bash 
h1 python UDPsend.py
```

### Observe PacketOut packets on the server 
Mininet will create a topology with 2 hosts and 1 server connected to a switch. The controller will for each received packetIn, generate a PacketOut and specify the output port as the 3rd port (hardcoded in the packetOut). 

```
$ sudo tcpdump -i s0-eth3
```

Expected output:
```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on s0-eth3, link-type EN10MB (Ethernet), capture size 262144 bytes
23:03:25.949165 IP 10.10.10.1.7777 > 10.10.3.3.80: UDP, length 24
23:03:25.988292 IP 10.10.10.1.7777 > 10.10.3.3.80: UDP, length 24
23:03:26.033244 IP 10.10.10.1.7777 > 10.10.3.3.80: UDP, length 24
23:03:26.068418 IP 10.10.10.1.7777 > 10.10.3.3.80: UDP, length 24
23:03:26.109795 IP 10.10.10.1.7777 > 10.10.3.3.80: UDP, length 24
```
