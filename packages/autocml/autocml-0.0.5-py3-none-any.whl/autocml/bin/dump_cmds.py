#!/usr/bin/env python3

from ipaddress import IPv4Interface
import sys
import os
import csv
from multiprocessing import Pool
from typing import Dict, List, Tuple, Optional
import netmiko
import virl2_client as virl

import autocml

# note: look at virl2_client.models.cl_pyalts.CLPyats

def usage():
	print("Usage: cml-dump-cmds <lab descriptor>", file=sys.stderr)
	exit(1)

def main():
	if len(sys.argv) != 2:
		usage()
	labdesc, = sys.argv[1:]

	client = autocml.client_from_env(ssl_verify=False)


	lab = autocml.resolve_lab(client, labdesc)
	if type(lab) == str:
		print(lab, file=sys.stderr)
		exit(1)

if __name__ == "__main__":
	main()
