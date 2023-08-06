
import sys
from multiprocessing import Pool
from ipaddress import IPv4Interface
from typing import Any, Dict, Optional
import netmiko
import virl2_client as virl
import virl2_client.models as virlty
from .connections import connect_to_device

def for_all(client: virl.ClientLibrary, lab: virlty.Lab, nodefunc, data=None, log_frame=True, processes=5) -> Dict[virlty.Node, Any]:
	"""
	Runs a callback function `nodefunc` for every node (with a console line) within the lab, in parallel

	Returns a dictionary of each node, and the return value of the `nodefunc` for that node.
	"""

	node_defs = { nd['id']: nd['data'] for nd in client.definitions.node_definitions() }

	with Pool(processes) as p:
		ents = (
			(nodefunc, log_frame, [client, node, data] if data is not None else [client, node])
			for node in lab.nodes()
			if node_defs[node.node_definition]['device']['interfaces']['serial_ports'] > 0
		)
		return dict(p.starmap(_for_all_wrapper, ents))

def _for_all_wrapper(func, log_frame, args):
	if log_frame: print(f"[{args[1].label}] begin", file=sys.stderr)
	rtn = func(*args)
	if log_frame: print(f"[{args[1].label}] finish", file=sys.stderr)
	return (args[1], rtn)


def collect_interfaces(client: virl.ClientLibrary, node: virlty.Node, conns: Optional[Dict[virlty.Node, netmiko.BaseConnection]] = None) -> Dict[str, Optional[IPv4Interface]]:
	"""
	Returns a dictionary of active interfaces, where the key is the interface name, and value is an IPv4Interface

	Should be passed an additional argument, either None or a Dict[Node, netmiko_conn] if you want to reuse an existing netmiko connection

	If there is no connection in the dict for this node, one will be inserted
	"""
	
	if not node.is_active():
		print(f"[{node.label}] not active; not collecting interface addresses")
		return None

	conn = get_connection(client, node, conns)
	
	conn.enable()
	ints = conn.send_command('show ip int', use_textfsm=True)
	
	rtn = dict()
	for int in ints:
		#print(int)
		if int['link_status'] == 'up':
			if len(int['ipaddr']) > 0 and len(int['mask']) > 0:
				rtn[int['intf']] = IPv4Interface(int['ipaddr'][0] + '/' + int['mask'][0])
			else:
				rtn[int['intf']] = None
		
	return rtn

def get_connection(client: virl.ClientLibrary, node: virlty.Node, conns=None) -> netmiko.BaseConnection:
	if conns is not None:
		if node in conns:
			return conns[node]
		else:
			conns[node]= connect_to_device(client, node)
			return conns[node]
	else:
		return connect_to_device(client, node)