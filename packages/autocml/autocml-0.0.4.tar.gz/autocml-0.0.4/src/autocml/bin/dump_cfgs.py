#!/usr/bin/env python3

import io
import os
import sys
from typing import List
import yaml
import virl2_client as virl
import autocml

def usage():
	print("Usage: cml-dump-cfgs <lab desc[.yaml]> <out folder>")
	print("Takes devices configurations from a lab/yaml and outputs them into a directory")
	print("First attempt will be read lab desc as a file. If there is no file by that name, the CML controller is seached for a lab by that description")
	print("If a lab is found on the CML controller, it's yaml will be downloaded (you may want to manually extract configs first)")
	exit(1)

def get_config(desc: str) -> str:
	""" Tries to read a file by that name, if it failes with ENOENT, check CML controller """

	try:
		with open(desc, "r") as f:
			return f.read()
	except OSError as e:
		assert e.strerror == "No such file or directory", "Received error reading yaml file: " + str(e)
		# no file by that name, look for it on CML controller
		pass

	client = autocml.client_from_env()
	
	lab = autocml.resolve_lab(client, desc)
	if type(lab) == str:
		print(lab, file=sys.stderr)
		exit(1)
	
	return lab.download()

def main():
	if len(sys.argv) != 3:
		usage()
	labdesc, outfolder = sys.argv[1:]
	
	if os.path.exists(outfolder):
		print("File/Folder already exists by the output folder's name. Remove it, or choose another one")
		exit(1)

	yamlstr = get_config(labdesc)

	try:
		labdata = yaml.safe_load_all(yamlstr)
	except yaml.YAMLError as e:
		print("There was an error reading the lab YAML: ", e)

	labdata = list(labdata)
	assert len(labdata) == 1, "No data within lab YAML"
	labdata = labdata[0]

	try:
		os.makedirs(outfolder, exist_ok=False)
	except OSError:
		print("File/Folder already exists by the output folder's name. Remove it, or choose another one")
		exit(1)

	title = labdata['lab']['title']
	for node in labdata['nodes']:
		conf = node.get('configuration')
		if conf is None: conf = ''
		conf.strip()

		if len(conf) > 0:
			filename = f"{node['label']}.cfg.txt"
			with open(os.path.join(outfolder, filename), 'w') as f:
				f.write(conf)


if __name__ == "__main__":
	main()




