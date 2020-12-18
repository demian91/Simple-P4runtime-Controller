# Simple-P4runtime-Controller

## Mininet with simple_switch_grpc
The scripts starts a very simple Mininet topo with just one switch. Additionally, it compiles the supplied P4 file to generate both the JSON as well as P4Info file (used by the controller)
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
python run_mininet.py --p4-file simple.p4
```
### Start the controller in a different terminal
```bash 
python controller.py
```
### Generate traffic (in Mininet)
```bash 
h1 python UDPsend.py
```
