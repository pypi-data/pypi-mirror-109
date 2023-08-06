#!/usr/bin/env python3

import io
import os
import sys
from typing import List
import virl2_client as virl
import autocml

def usage():
	print("Usage: cml-pcap <cml lab> <out.pcap> <link regex>")
	print("Starts a packet capture on multiple links, and outputs them as a single pcap file.")
	print("Links can be matched via a regex, where they are being matched against `node A label-node B label`")
	print("Note that each link has a reflexive version matched as well.")
	print("For example, a link between 'R1' and 'R2' will be matched as both 'R1-R2' and 'R2-R1'")
	print("The capture can be stopped with ctrl-c")
	exit(1)

def main():
	host, user, passwd = autocml.from_env()
	if len(sys.argv) != 2:
		usage()
	outfolder, = sys.argv[1:]
	
	raise RuntimeError("not yet implemented")

	try:
		os.makedirs(outfolder, exist_ok=False)
	except OSError:
		print("folder already exists. remove it or choose another one")
		usage()

	client = virl.ClientLibrary(host, user, passwd, ssl_verify=False)

	labs: List[virl.virl2_client.Lab] = client.all_labs(show_all=True)
	for lab in labs:
		with io.open(os.path.join(outfolder, f"{lab.id}.{lab.title}.yaml"), "w") as f:
			f.write(lab.download())

if __name__ == "__main__":
	main()
