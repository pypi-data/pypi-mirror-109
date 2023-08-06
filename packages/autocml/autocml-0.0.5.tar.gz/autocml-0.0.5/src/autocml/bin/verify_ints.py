#!/usr/bin/env python3

from ipaddress import IPv4Interface
import sys
import csv
import json
import argparse
from typing import Dict, List, Tuple, Optional
import virl2_client as virl
import virl2_client.models as virlty

import autocml

description=[
	"Retrieves device interface addresses, and asserts them against a CSV file. ",
	"Can also dump interface addresses to stdout for later comparison."
]

def optparser():
	parser = argparse.ArgumentParser(
		description='\n'.join(description),
		parents=[autocml.argparse.root_parser()]
	)

	autocml.argparse.add_lab_desc(parser)

	parser.add_argument('-j', '--json',
		dest='json',
		action='store_true', 
		help='Output results in JSON format'
	)
	parser.add_argument('-d', '--dump',
		dest='dump',
		action='store_true', 
		help="Scrape the labs' nodes' interfaces and output it to stdout (ignores interface_csv argument)"
	)
	parser.add_argument('interface_csv',
		nargs='?',
		help='A comma-seperated-value file, containing rows of "Node Label", "Int", "IPv4"'
	)

	return parser

def parse_ip_assertions(intfile: str) -> Dict[str, Dict[str, Optional[IPv4Interface]]]:
	""" Parses the specified csv file from disk into Dict[device, Dict[interface, address]]"""

	checks: Dict[str, Dict[str, Optional[IPv4Interface]]] = dict()
	csv_data = sys.stdin if intfile == '-' else open(intfile)

	for li, entry in enumerate(csv.reader(csv_data)):
		if li == 0:
			assert entry == ['Node Label', 'Int', 'IPv4'], "Passed interface file is not a valid tab seperated interface descriptor file"
		else:
			if len(entry) == 3:
				device, int, ip = entry
				if device not in checks:
					checks[device] = dict()

				if len(ip.strip()) == 0 or ip == '-':
					checks[device][int] = None	
				else:
					checks[device][int] = IPv4Interface(ip)
				
				if '/' not in ip and ip != '-':
					print(f"[lint][{intfile}:{li+1}] the IP for {device}.{int} ({ip}) is missing a CIDR-notation subnet", file=sys.stderr)
			elif len(entry) == 0:
				pass # ignore blank lines
			else:
				print(f"[lint][{intfile}:{li+1}] the entry `{repr(entry)}` does not have exactly three values (Node Label, Int, IPv4)", file=sys.stderr)

	csv_data.close()

	return checks

def print_node_results(node: virlty.Node, ints: Dict[str, Optional[IPv4Interface]], checks: Dict[str, Optional[IPv4Interface]], emit_json: bool = False):
	for usrint, exp_addr in checks.items():
		for iosint, act_addr in ints.items():
			if autocml.interface_matches(iosint, usrint):
				matches = act_addr == exp_addr

				if emit_json:
					data = {
						'node': node.label,
						'interface': iosint,
						'address': '-' if act_addr is None else str(act_addr),
						'matches': matches,
					}
					if not matches: data['expected'] = '-' if exp_addr is None else str(exp_addr)

					print(json.dumps(data))
				else:
					if act_addr == exp_addr:
						print(f"[{node.label}][{iosint}] ✔️   ({str(act_addr)})")
					else:
						print(f"[{node.label}][{iosint}] ❌   (found {act_addr}, expected {exp_addr})")
				
				break
		else:
			print(f"[lint][{node.label}][{iosint}] unable to resolve interface")

def main(pargs=None):
	parser = optparser()
	args = parser.parse_args(pargs)

	# if args.test_args:
	# 	print(args)
	# 	return 1

	if args.dump and args.interface_csv:
		parser.error("cannot pass an interface file when dumping")
	elif not args.dump and not args.interface_csv:
		parser.error("requires an interface file when verifying")

	client = autocml.get_client(args)

	labdesc, intfile = args.lab_description, args.interface_csv

	lab = autocml.resolve_lab(client, labdesc)
	if type(lab) == str:
		print(lab, file=sys.stderr)
		exit(1)

	if not args.dump:
		checks = parse_ip_assertions(intfile)

		checksbynode = dict()
		for nodedesc in checks.keys():
			try:
				node = lab.get_node_by_label(nodedesc)
				checksbynode[node] = checks[nodedesc]
			except virl.NodeNotFound:
				print(f"Unable to find node by descriptor '{nodedesc}' on {args.user}@{client.get_host()}/{lab.id} (ignoring node, continuing)")

		ints = autocml.for_all(client, lab, autocml.parallel.collect_interfaces, processes=len(lab.nodes()))

		for node, ints in sorted(ints.items(), key=lambda ent: ent[0].label):
			if node in checksbynode:
				if ints is None:
					if not args.json: print(f"\tcould not collect interfaces; not checking")
					continue

				if not args.json: print(f"******** {node.id}/{node.label} on {node.lab.id}/{node.lab.title}")
				
				#ints = node_interfaces(client, node)
				print_node_results(node, ints, checksbynode[node], emit_json=args.json)

	else:
		# dump it all
		ints = autocml.for_all(client, lab, autocml.parallel.collect_interfaces, processes=len(lab.nodes()))

		file = sys.stdout
		if not args.json:
			
			writer = csv.writer(file)
			writer.writerow(['Node Labels', 'Int', 'IPv4'])
			for node, ints in sorted(ints.items(), key=lambda e: e[0].label):
				for int, addr in sorted(ints.items(), key=lambda e: e[0]):
					writer.writerow([node.label, int, '-' if addr is None else str(addr)])
		
				
		else:
			for node, ints in sorted(ints.items(), key=lambda e: e[0].label):
				for int, addr in sorted(ints.items(), key=lambda e: e[0]):
					file.write(json.dumps({
						'node': node.label,
						'interface': int,
						'address': '-' if addr is None else str(addr),
					}) + '\n')

		if file != sys.stdout:
			file.close()




if __name__ == "__main__":
	main()


