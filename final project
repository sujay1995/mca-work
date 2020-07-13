from __future__ import print_function

import array

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp, tcp, udp
from ryu.lib import snortlib
from ryu.controller import dpset



class SimpleSwitchSnort(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        'snortlib': snortlib.SnortLib,
        'dpset': dpset.DPSet,
    }

    def __init__(self, *args, **kwargs):
        super(SimpleSwitchSnort, self).__init__(*args, **kwargs)
        self.snort = kwargs['snortlib']
        self.dpset = kwargs['dpset']
        self.snort_port = 3
        self.mac_to_port = {}

        socket_config = {'unixsock': True}

        self.snort.set_config(socket_config)
        self.snort.start_socket_server()
    def packet_print(self, pkt):  
        pkt = packet.Packet(array.array('B', pkt))

        eth = pkt.get_protocol(ethernet.ethernet)   #gets packet info from ryu packet library
        _ipv4 = pkt.get_protocol(ipv4.ipv4)
        _icmp = pkt.get_protocol(icmp.icmp)

        if _icmp:
            self.logger.info("%r", _icmp)

        if _ipv4:
            self.logger.info("%r", _ipv4)

        if eth:
            self.logger.info("%r", eth)

       


    def send_divert_flowrule(self, msg):
        

        #datapath = self.datapath
        dpid = 3 
        datapath = self.dpset.get(dpid)

        if datapath is None:
            self.logger.info('')
            return


        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(array.array('B',msg.pkt))
        # pkt_eth = pkt.get_protocol(ethernet.ethernet)

        # mac_src = pkt_eth.src
        #eth_type = pkt_eth.ethertype

        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        if pkt_ipv4:
            ip_proto = pkt_ipv4.proto
            # src = pkt_ipv4.src
            pkt_tcp = pkt.get_protocol(tcp.tcp)
            pkt_udp = pkt.get_protocol(udp.udp)
           # pkt_icmp = pkt.get_protocol(icmp.icmp)

         #TCP flow
        if pkt_tcp:
            self.logger.info(' tcp packet')
            
            # print('matching flow')
            match = parser.OFPMatch(eth_type=0x800, ipv4_dst="10.0.0.4")
            # match = parser.OFPMatch(eth_type=0x800, ipv4_src="10.0.0.2", ipv4_dst="10.0.0.4")
            # print ("1")
        elif pkt_udp:
            self.logger.info(' udp packet')
          
            # print('matching flow')
            match = parser.OFPMatch(eth_type=0x800, ipv4_src="10.0.0.1",ipv4_dst="10.0.0.4")
            # match = parser.OFPMatch(eth_type=0x800, ipv4_src="10.0.0.2",ipv4_dst="10.0.0.4")

            # print ("3")

        # elif pkt_icmp:
        #     self.logger.info('icmp packet')   #ICMP PACKET
        #     match1 = parser.OFPMatch(in_port=2 or 3,eth_src=mac_src,
        #                             eth_type=0x800, ipv4_dst="10.0.0.4", ipv4_src=pkt_ipv4.src,
        #                             ip_proto=ip_proto)
        # print ("4")
       
        # print('5')
        priority = 100
        actions = [parser.OFPActionOutput(2)] # actions to apply
        # print ('adding flow')    
        #print('here')
        self.add_flow(datapath, priority, match, actions)
    
    def add_flow(self, datapath, priority, match, actions, idle_timeout=0, hard_timeout=0, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath = datapath, buffer_id = buffer_id, 
            priority = priority, match = match, instructions = inst, idle_timeout = idle_timeout, hard_timeout = hard_timeout)
        else:
            mod = parser.OFPFlowMod(datapath = datapath, priority = priority, 
            match = match, instructions = inst, idle_timeout = idle_timeout, hard_timeout = hard_timeout)
        
        datapath.send_msg(mod) 

        # dpid = 2 
        # datapath = self.dpset.get(dpid)
        # ofproto = datapath.ofproto

        # parser = datapath.ofproto_parser

        # match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src1="10.0.0.1", ipv4_src2 ="10.0.0.2")
        # print("rcvd")

        # actions = [parser.OFPActionOutput(2)]

        # inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        # self.add_flow(datapath, priority, match, actions)
    

            

    #main dispatcher for snort alert events
    @set_ev_cls(snortlib.EventAlert, MAIN_DISPATCHER) 
    def process_snort_alert(self, ev):
        # self._dump_alert(ev)
        msg = ev.msg
        alertmsg = ''.join(msg.alertmsg)
        if 'ryu has blocked' in alertmsg:
            self.logger.info('********flow diverted!***********{0}'.format(alertmsg))
            self.send_divert_flowrule(msg)  #calls the divert flow func when if cond is met

    def _dump_alert(self, ev):
        msg = ev.msg

        # print('alertmsg: %s' % ''.join(msg.alertmsg))

        self.packet_print(msg.pkt)
      #defs add flow 
    

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath   #switch datapath obj instance
        self.datapath = datapath
        self.logger.info('add datapath id: {0}'.format(datapath.id))
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser  #switch message parser

       
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port),
                   parser.OFPActionOutput(self.snort_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
