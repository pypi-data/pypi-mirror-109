#!/usr/bin/env python3

import re
import os
import sys
import base64
import subprocess
from time import sleep
from typing import List, Tuple
import requests

import virl2_client as virl
from virl2_client.models.lab import Lab
from virl2_client.models.node import Node

from ..auth import client_from_env

mobaxterm="MobaXterm_Professional_9.4.exe"

def main():
	args = sys.argv[1:]
	term = "wt" # default
	noverify=False
	labreg = None
	nodereg = None

	while len(args) > 0:
		head = args.pop(0)
		if head == "--term":
			term = args.pop(0)
		elif head == "--nosslverify":
			noverify = True
		elif labreg == None:
			labreg = head
		elif nodereg == None:
			nodereg = head
		else:
			# too many args
			print_usage("unrecognized argument")
			exit(1)
	
	if labreg == None:
		print_usage("no lab specified")
		return

	# print(locals())
	try:
		cl = client_from_env(ssl_verify=not noverify)
	except requests.exceptions.SSLError as e:
		if "CERTIFICATE_VERIFY_FAILED" in str(e):
			print(str(e))
			print()
			print("Error authenticating CML host SSL certificate. Is it self signed? Try passing --nosslverify")
			exit(1)
		else:
			raise e

	cl._make_test_auth_call()

	(lab, nodes) = find_lab_nodes(labreg, nodereg, cl)

	open_term(term, lab, nodes, cl)

def open_term(term: str, lab: Lab, nodes: List[Node], client: virl.ClientLibrary):
	env=os.environ.copy()
	env.update({
		"CML_HOST": client.get_host(),
		"CML_USER": client.username,
		"CML_PASS64": base64.b64encode(bytes(client.password, "utf-8")).decode("utf-8")
	})
	paths = [f"/{lab.id}/{node.id}" for node in nodes]

	if "mobaxterm" in term.lower():
		# launch the first process, wait 15s, launch rest
		for i, path in enumerate(paths):
			if i >= 1:
				waittime = 30 if i == 1 else 2
				print("sleeping "+str(waittime)+"s before sending next node command...")
				sleep(waittime)
				#print("done sleeping "+str(waittime))

			# start each proces, without waiting for it to finish
			subprocess.Popen(
				[term, "-newtab", "cmd.exe /drives/c/Users/thewh/.cargo/bin/cmlterm.exe open --boot " + path],
				shell=False,
				env=env,
			)
	elif re.match("wt\\b", term):
		subcmds = [["new-tab", "cmlterm", "open", "--boot", path] for path in paths]
		flattened = []
		for i, subcmd in enumerate(subcmds):
			flattened.extend(subcmd)
			if i+1 != len(subcmds):
				flattened.append(";")
		
		subprocess.run(
			[term, *flattened],
			shell=False,
			env=env,
		)
	elif re.match("cmd\\b", term):
		for path in paths:
			print(f"Opening {path}...")
			subprocess.run(
				["start", term, "/c", "derp.bat", path],
				shell=True,
				env=env,
			)
	else:
		print_usage("terminal not found")
		exit(1)

def find_lab_nodes(labreg, nodereg, client) -> Tuple[Lab, List[Node]]:
	lab = None

	labregex = re.compile(labreg)
	labs: List[Lab] = client.all_labs(show_all=True)
	for labobj in labs:
		if labreg == labobj.id or labreg in labobj.title or labregex.search(labobj.title):
			lab = labobj
			break
	
	if lab is None:
		print("Unable to find lab for ID/regex " + repr(labreg))
		exit(1)

	rtn_nodes = list()
	nodes: List[Node] = lab.nodes()
	if nodereg:
		noderegex = re.compile(nodereg)
		for nodeobj in nodes:
			if nodereg == nodeobj.id or nodereg in nodeobj.label or noderegex.search(nodeobj.label):
				rtn_nodes.append(nodeobj)
	else:
		rtn_nodes = nodes

	if len(rtn_nodes) == 0:
		print(f"No nodes found for regex: {repr(nodereg)} in lab {repr(lab.title)} ({lab.id}). Not launching terminal.")
		exit(1)

	node_defs = { nd['id']: nd['data'] for nd in client.definitions.node_definitions() }
	return (lab, [node for node in rtn_nodes if node_defs[node.node_definition]['device']['interfaces']['serial_ports'] > 0])

def get_cml_env() -> Tuple[str, str, str]:
	env = os.environ
	host = (env.get("CML_HOST"), env.get("BREAKOUT_CONTROLLER"))
	user = (env.get("CML_USER"), env.get("BREAKOUT_USERNAME"))
	pass64 = env.get("CML_PASS64")
	passwd = (env.get("CML_PASS"), env.get("BREAKOUT_PASSWORD"))
	
	try:
		rtn_host = next(h for h in host if h is not None)
	except StopIteration:
		print("No CML_HOST or BREAKOUT_CONTROLLER environment variables found", file=sys.stderr)
		exit(1)

	try:
		rtn_user = next(u for u in user if u is not None)
	except StopIteration:
		print("No CML_USER or BREAKOUT_USERNAME environment variables found", file=sys.stderr)
		exit(1)

	if pass64 is not None:
		rtn_pass = base64.b64decode(pass64).decode("utf-8")
	else:
		rtn_pass = next(p for p in passwd if p is not None)

	# ensure all are populated
	if not all([rtn_host, rtn_user, rtn_pass]):
		print("Not all host environment variables present. Must have:")
		print("CML_HOST or BREAKOUT_CONTROLLER: CML host IP/address")
		print("CML_USER or BREAKOUT_USERNAME: The username of the CML user")
		print("CML_PASS64 or CML_PASS or BREAKOUT_PASSWORD: The password of the CML user (where CML_PASS64 is in base64 format)")
		exit(1)

	return (rtn_host, rtn_user, rtn_pass)

def print_usage(err):
	exe = sys.argv[0]
	if err:
		print(f"Error: " + err)
	print(f"Usage: {exe} [--nosslverify] [--term mobaxterm|wt|cmd] <lab ID/name regex> [node ID/name regex]")
	print()
	print("Opens nodes of a specific lab (if regex provided, then first matching) as seperate tabs within the chosen terminal.")
	print()
	print(f"Uses windows terminal by default. (Mobaxterm specifically searches for {mobaxterm}")
	print(f"--term specifies the terminal binary, (either by path or in the PATH) customizing the command line if needed")
	print(f"\tif the terminal is unrecognized, it will print a warning and run a new command for each console requested")
	print("Requires cmlterm to be installed, as well as the specified terminal")
	print()


if __name__ == "__main__":
	main()

