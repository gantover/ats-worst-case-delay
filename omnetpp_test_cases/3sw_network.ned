package dtu_networks;

import inet.networks.base.TsnNetworkBase;
import inet.node.ethernet.Eth1G;
import inet.node.tsn.TsnDevice;
import inet.node.tsn.TsnSwitch;

network ring_3sw_network extends TsnNetworkBase {
    @display("bgb=1500,1000");
    submodules:
        sw_0: TsnSwitch {
            @display("p=729,444");
        }
        sw_1: TsnSwitch {
            @display("p=884,498");
        }
        sw_2: TsnSwitch {
            @display("p=902,390");
        }
        node_0_0: TsnDevice {
            @display("p=633,344");
        }
        node_0_1: TsnDevice {
            @display("p=633,544");
        }
        node_1_0: TsnDevice {
            @display("p=1012,553");
        }
        node_2_0: TsnDevice {
            @display("p=1041,344");
        }
    connections:
        sw_0.ethg++ <--> Eth1G <--> sw_1.ethg++;
        sw_0.ethg++ <--> Eth1G <--> sw_2.ethg++;
        sw_0.ethg++ <--> Eth1G <--> node_0_0.ethg++;
        sw_0.ethg++ <--> Eth1G <--> node_0_1.ethg++;
        sw_1.ethg++ <--> Eth1G <--> sw_2.ethg++;
        sw_1.ethg++ <--> Eth1G <--> node_1_0.ethg++;
        sw_2.ethg++ <--> Eth1G <--> node_2_0.ethg++;
}
