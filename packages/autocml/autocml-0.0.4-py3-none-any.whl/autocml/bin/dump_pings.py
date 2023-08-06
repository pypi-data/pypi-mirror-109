#!/usr/bin/env python3

import sys
import os
import re
import csv
from multiprocessing import Pool
from typing import Any, Dict, List, Tuple
import netmiko
import virl2_client as virl
import autocml

def usage():
	print("Usage: cml-dump-pings <lab descriptor> [out folder]")
	print("Extracts the interface addresses from each machine,")
	print("and pings them all from every other device")
	print("Ping logs are output to the output folder as `{node label}.pings.txt`")
	print("If the output folder name is omitted, then the lab's title is used")
	print("Any ping failures are output to stderr.")
	exit(1)

def ping_from(client, node, args):
	outfolder, targets = args
	if node not in targets.keys():
		return
	
	conn = autocml.connect_to_device(client, node)
	with open(f"{outfolder}/{node.label}.pings.txt", "w") as f:
		for dstnode, dstints in sorted(targets.items(), key=lambda tup: tup[0].label):
			if dstnode != node:
				for dstint, dstip in sorted(dstints.items(), key=lambda tup: tup[0]):
					pingcmd = f'ping {dstip} ! to {dstnode.label}.{dstint}'
					# print(pingcmd, file=sys.stderr)
					output = conn.send_command(pingcmd, strip_prompt=False, strip_command=False)
					print(conn.find_prompt() + ' ' + output, file=f)
					if 'Success rate is 100 percent' not in output:
						print(f'!!!!!!!!!!!!!! PING FAILED !!!!!!!!!!!!!! ' + node.label + "# " + pingcmd, file=sys.stderr)
					conn.send_command('')

def scrape_ints(client: virl.ClientLibrary, node):
	conn = autocml.connect_to_device(client, node)
		
	raw_ints = conn.send_command('show ip int brief', use_textfsm=True)

	return {
		int['intf']: int['ipaddr']
		for int in raw_ints
		# if int['intf'].startswith('Loopback')
		if int['ipaddr'] != 'unassigned'
	}

def main():
	client = autocml.client_from_env()

	if len(sys.argv) != 2 and len(sys.argv) != 3:
		usage()
	if len(sys.argv) == 2:
		labdesc,  = sys.argv[1:]
		outfolder = None # labname
	elif len(sys.argv) == 3:
		labdesc, outfolder = sys.argv[1:]
	else:
		usage()

	lab = autocml.resolve_lab(client, labdesc)
	if type(lab) == str:
		print(lab, file=sys.stderr)
		exit(1)

	if outfolder is None:
		outfolder = lab.title

	os.makedirs(outfolder, exist_ok=True)

	print(f"Scraping interfaces...", file=sys.stderr)
	ints = autocml.for_all(client, lab, scrape_ints)

	print(f"Pinging...", file=sys.stderr)
	autocml.for_all(client, lab, ping_from, (outfolder, ints))

	print(f"Done")

if __name__ == "__main__":
	main()

