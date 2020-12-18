# Simple-P4runtime-Controller

## Mininet with simple_switch_grpc
The scripts start a very simple Mininet topo with just 1 switch. Adiditonaly, it compules the supplied P4 file to generate both the json as well as P4Info file (used by the contorller)
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
At the start of the connection the controller installs a 3 rules, forwarding the packets to the CPU port. Furthermore, it listens to PacketIn messages and outputs them to the port 3. 
```bash 
##Packet-In messages
 @controller_header("packet_in")
 header packet_in_t {
    bit<16> ingress_port;
 }
 ```

##Packet-Out messages
```bash 
 @controller_header("packet_in")
 header packet_in_t {
     bit<16> ingress_port;
 }
 ```
Transalates to the metadata values seen at the output of the controller.
## Run a test scenario

###Start Mininet (with simple_switch_grpc)
```bash 
python run_mininet.py --p4-file simple.p4
```
###Start the controller in a different terminal
```bash 
python controller.py
```
###Generate traffic (in Mininet)
```bash 
h1 python UDPsend.py
```
