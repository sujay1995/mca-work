///transport layer firewall
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import logging
from ryu.ofproto import ether
import random
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.app import simple_switch_13
import csv
import os
from ryu.lib import addrconv
#Pingall requried before trying load balancing functionality
AllowFile = "%s/Allowance.csv" % os.environ[ 'HOME' ]	

class ShareIt(app_manager.RyuApp):
	
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
        	super(ShareIt, self).__init__(*args, **kwargs)
        	self.mac_to_port = {}
		self.ip_to_port = {}
		#Add the configuration file inside the Home directory
		with open(AllowFile) as csvfile:
			self.rules = csv.DictReader(csvfile)	
		self.logger.info("Initialized new Object instance data")

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, ev):
		datapath = ev.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		# install table-miss flow entry
		#
		# We specify NO BUFFER to max_len of the output action due to
		# OVS bug. At this moment, if we specify a lesser number, e.g.,
		# 128, OVS will send Packet-In with invalid buffer_id and 
		# truncated packet data. In that case, we cannot output packets
		# correctly.  The bug has been fixed in OVS v2.1.0.
		match = parser.OFPMatch()
		actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
		self.add_flow(datapath, 0, match, actions)
		self.logger.info("Set Config data for new Object Instance")

	def ipv4_to_int(self, string):
        	ip = string.split('.')
        	assert len(ip) == 4
        	i = 0
        	for b in ip:
			b = int(b)
            		i = (i << 8) | b
        	return i

	def add_flow(self, datapath, priority, match, actions, buffer_id=None):
		self.logger.info("Now adding flow")
		ofproto = datapath.ofproto
        	parser = datapath.ofproto_parser

        	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        	if buffer_id:
			mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id, priority=priority, match=match, instructions=inst)
        	else:
            		mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        	datapath.send_msg(mod)
		self.logger.info("Done adding flows")
	
	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _packet_in_handler(self, ev):
		self.logger.info("Entered main mode event handling")
        	# If you hit this you might want to increase
        	# the "miss_send_length" of your switch
        	if ev.msg.msg_len < ev.msg.total_len:
        		self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
							  
		self.logger.info("Will print data now")					  
		#print event data
		
        	#fetch all details of the event
		msg = ev.msg
	       	datapath = msg.datapath
       		ofproto = datapath.ofproto
       		parser = datapath.ofproto_parser
       		in_port = msg.match['in_port']
		dpid = datapath.id

       		pkt = packet.Packet(msg.data)
       		eth = pkt.get_protocols(ethernet.ethernet)[0]

        	dst = eth.dst
       		src = eth.src
		

        	dpid = datapath.id
        	self.mac_to_port.setdefault(dpid, {})
        	self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)		

		# learn a mac address to avoid FLOOD next time.
                self.mac_to_port[dpid][src] = in_port    
		self.logger.info("Ether Type: %s", eth.ethertype)
		if eth.ethertype == ether_types.ETH_TYPE_LLDP:
			# ignore lldp packet
			return
			
		if eth.ethertype == 2054:
			arp_head = pkt.get_protocols(arp.arp)[0]
			if True: #redundant line	
				dst = eth.dst
                        	src = eth.src

                        	dpid = datapath.id
                        	self.mac_to_port.setdefault(dpid, {})

                        	self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

                        	# learn a mac address to avoid FLOOD next time.
                        	self.mac_to_port[dpid][src] = in_port

                        	if dst in self.mac_to_port[dpid]:
                                	out_port = self.mac_to_port[dpid][dst]
                        	else:
                                	out_port = ofproto.OFPP_FLOOD

                       		actions = [parser.OFPActionOutput(out_port)]

                        	# install a flow to avoid packet_in next time
                        	if out_port != ofproto.OFPP_FLOOD:
                                	match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_type=0x0806)
                                	# verify if we have a valid buffer_id, if yes avoid to send both
                                	# flow_mod & packet_out
                                	if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                                        	self.add_flow(datapath, 2, match, actions, msg.buffer_id)
                                        	return
                                	else:
                                        	self.add_flow(datapath, 2, match, actions)
                        	data = None
                        	if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                                	data = msg.data

                        	out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  	in_port=in_port, actions=actions, data=data)
                        	datapath.send_msg(out)
                       		return
	
		
		try:
			if pkt.get_protocols(icmp.icmp)[0]:
		
			#if ip_head.proto == inet.IPPROTO_ICMP:
				dst = eth.dst
		        	src = eth.src

				dpid = datapath.id
				ip = pkt.get_protocols(ipv4.ipv4)[0]
				sip = ip.src
				dip = ip.dst
				self.ip_to_port.setdefault(dpid, {})
				self.ip_to_port[dpid][sip] = in_port   		
		        	
        			self.mac_to_port.setdefault(dpid, {})

        			self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
				self.logger.info("ICMP being Handled")
       				# learn a mac address to avoid FLOOD next time.
        			self.mac_to_port[dpid][src] = in_port

        			if dst in self.mac_to_port[dpid]:
        				out_port = self.mac_to_port[dpid][dst]
        			else:
            				out_port = ofproto.OFPP_FLOOD
	
        			actions = [parser.OFPActionOutput(out_port)]

        			# install a flow to avoid packet_in next time
        			if out_port != ofproto.OFPP_FLOOD:
            				match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_type=0x0800, ip_proto=0x01)
            				# verify if we have a valid buffer_id, if yes avoid to send both
            				# flow_mod & packet_out
            				if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                				self.add_flow(datapath, 2, match, actions, msg.buffer_id)
                				return
            				else:
                				self.add_flow(datapath, 2, match, actions)
        			data = None
        			if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            				data = msg.data

        			out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        			datapath.send_msg(out)
				return

		except:
			pass
		
		#if self.check == 1:
		#	print "Check = 1"
		#	return
		#ip_head = pkt.get_protocols(ipv4.ipv4)[0]
		#tcp_head = pkt.get_protocols(tcp.tcp)[0]
		# learn a mac address to avoid FLOOD next time.
		#self.mac_to_port[dpid][src] = in_port
		
		eth = pkt.get_protocols(ethernet.ethernet)[0]
                dst = eth.dst
                src = eth.src
                dpid = datapath.id
		print "Let's start the Firewall..."
		priority=10
		with open(AllowFile) as csvfile:
			print "Reading CSV File Again... Verifying"
			self.rules=csv.DictReader(csvfile)
			for row in self.rules:
				print "Fetching values..."
				s_ip=row['src_ip']
				d_ip=row['dst_ip']
				s_port=row['src_port']
				d_port=row['dst_port']
				print "Values Fetched: %s,%s <--> %s,%s" % (s_ip,s_port,d_ip,d_port)
				print "Deciding the Match fields and Reverse Match Fields..."
				if s_ip == "any" and d_ip != "any" and s_port != "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=d_ip, tcp_src=int(s_port), tcp_dst=int(d_port))
					match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=d_ip, tcp_src=int(d_port), tcp_dst=int(s_port))
				elif s_ip != "any" and d_ip == "any" and s_port != "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, tcp_src=int(s_port), tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, tcp_src=int(d_port), tcp_dst=int(s_port))
				elif s_ip != "any" and d_ip != "any" and s_port == "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, ipv4_dst=d_ip, tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, ipv4_src=d_ip, tcp_src=int(d_port))
				elif s_ip != "any" and d_ip != "any" and s_port != "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, ipv4_dst=d_ip, tcp_src=int(s_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, ipv4_src=d_ip, tcp_dst=int(s_port))
				elif s_ip != "any" and d_ip != "any" and s_port == "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, ipv4_dst=d_ip)
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, ipv4_src=d_ip)
				elif s_ip != "any" and d_ip == "any" and s_port == "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip)
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip)
				elif s_ip == "any" and d_ip != "any" and s_port == "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=d_ip)
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=d_ip)
				elif s_ip != "any" and d_ip == "any" and s_port == "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, tcp_src=int(d_port))
				elif s_ip != "any" and d_ip == "any" and s_port != "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, tcp_src=int(s_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=s_ip, tcp_dst=int(s_port))
				elif s_ip == "any" and d_ip != "any" and s_port == "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=d_ip, tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=d_ip, tcp_src=int(d_port))
				elif s_ip == "any" and d_ip != "any" and s_port != "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_dst=d_ip, tcp_src=int(s_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=d_ip, tcp_dst=int(s_port))
				elif s_ip == "any" and d_ip == "any" and s_port == "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_src=int(d_port))
				elif s_ip == "any" and d_ip == "any" and s_port != "any" and d_port == "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_src=int(s_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_dst=int(s_port))
				elif s_ip == "any" and d_ip == "any" and s_port != "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_src=int(s_port), tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, tcp_dst=int(s_port), tcp_src=int(d_port))
				elif s_ip != "any" and d_ip != "any" and s_port != "any" and d_port != "any":
					match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=s_ip, ipv4_dst=d_ip, tcp_src=int(s_port), tcp_dst=int(d_port))
                                        match_rev = parser.OFPMatch(eth_type=0x0800, ip_proto=0x06, ipv4_src=d_ip, ipv4_dst=s_ip, tcp_src=int(d_port), tcp_dst=int(s_port))
				else:
					match = parser.OFPMatch()
					match_rev = parser.OFPMatch()

				#self.logger.info("Forward Match fields: ", str(match))
				#self.logger.info("Reverse Match fields: ", str(match_rev))
				#if d_ip != "any":
				#	if dst in self.mac_to_port[dpid]:
                                #       	out_port = self.mac_to_port[dpid][dst]
                                #	else:
                                #        	out_port = ofproto.OFPP_FLOOD
				#else:
				out_port=ofproto.OFPP_FLOOD
				#print "Port to be forwarded", self.ip_to_port[dpid][d_ip]
				actions = [parser.OFPActionOutput(out_port)]
                                print "Adding Flows for Forward Flow"
				self.add_flow(datapath, priority, match, actions)
                                priority += 1
				#if s_ip != "any":
                                #        if src in self.mac_to_port[dpid]:
                                #                out_port = self.mac_to_port[dpid][src]
                                #        else:
                                #                out_port = ofproto.OFPP_FLOOD
                                #else:
                                #        out_port=ofproto.OFPP_FLOOD

                                actions2 = [parser.OFPActionOutput(out_port)]
				#print "Port to be forwarded during reverse flow", self.mac_to_port[dpid][s_ip]
				print "Adding Flows for Reverse Flow"
				self.add_flow(datapath, priority, match_rev, actions2)
				priority += 1

				data = None
                                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                                        data = msg.data
				print "Sending PacketOut message"
                                out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
                                datapath.send_msg(out)

		self.logger.info("DROP other TCP traffic")
                match=parser.OFPMatch(eth_type=0x0800, ip_proto=0x06)
                instruction=[parser.OFPInstructionActions(ofproto.OFPIT_CLEAR_ACTIONS, [])]
                mod=parser.OFPFlowMod(datapath=datapath, priority=5, command=ofproto.OFPFC_ADD, match=match, instructions=instruction)
                datapath.send_msg(mod)

                self.logger.info("DROP UDP traffic")
                match=parser.OFPMatch(eth_type= 0x0800, ip_proto=0x17)
                instruction=[parser.OFPInstructionActions(ofproto.OFPIT_CLEAR_ACTIONS, [])]
                mod=parser.OFPFlowMod(datapath=datapath, priority=4, command=ofproto.OFPFC_ADD, match=match, instructions=instruction)
                datapath.send_msg(mod)
