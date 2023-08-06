
import os
import re
import sys
import base64
from time import sleep
from multiprocessing import Pool
from typing import Counter, Tuple, List, Optional, Union
import netmiko
import virl2_client as virl
import virl2_client.models as virl_ty

def resolve_lab(client: virl.ClientLibrary, labdesc: str, user: str=None) -> Union[virl_ty.Lab, str]:
	"""
	Finds the first lab on the CML server that matches by ID or title

	If it partially matches multiple labs at the beginning, it will return one after enough letters are given to disambiguate

	If no matches are found, a string describing the error is returned.
	"""

	# check for (in this order):
	# * exact ID
	# * exact title
	# * partial title
	# * partial ID

	if user == None:
		user = client.username

	labs: List[virl.virl2_client.Lab] = client.all_labs(user != client.username)
	
	# search by ID
	by_id = {
		lab.id: lab
		for lab in labs
		if lab.owner == user and lab.id.startswith(labdesc)
	}

	# search exact ID
	if labdesc in by_id.keys():
		return by_id[labdesc]

	by_title = {
		lab.title: lab
		for lab in labs
		if lab.owner == user and lab.title.startswith(labdesc)
	}

	# search exact title
	if labdesc in by_title.keys():
		return by_title[labdesc]

	# search best batch title
	best_title_list = list()
	best_title_len = 0
	for title in by_title.keys():
		if len(title) > best_title_len:
			best_title_list = list()
		elif len(title) < best_title_list:
			continue

		best_title_list.append(title)

	if len(best_title_list) == 1:
		return by_title[best_title_list[0]]
	elif len(best_title_list) > 1:
		return f"Unable to find lab by descriptor {labdesc} on {user}@{client.get_host()} - too many lab titles match"



	# search best batch ID
	best_id_list = list()
	best_id_len = 0
	for id in by_id.keys():
		if len(id) > best_id_len:
			best_id_list = list()
		elif len(id) < best_id_list:
			continue

		best_id_list.append(title)

	multiple_id_matches = False

	if len(best_id_list) == 1:
		return by_id[best_id_list[0]]
	elif len(best_id_list) > 1:
		return f"Unable to find lab by descriptor {labdesc} on {user}@{client.get_host()} - too many lab IDs match"

	return f"Unable to find lab by descriptor {labdesc} on {user}@{client.get_host()} - no labs match"

def connect_to_device(client: virl.ClientLibrary, node: virl_ty.Node) -> netmiko.BaseConnection:
	""" Connects to a device using Netmiko over CML's SSH interface, and returns the connection """
	conn = netmiko.ConnectHandler(device_type='terminal_server',
		host=client.get_host(),
		username=client.username,
		password=client.password,
	)

	conn.write_channel('\r')
	conn.write_channel(f'open /{node.lab.id}/{node.id}/0\r')

	#conn.write_channel('\r\n')
	sleep(0.5)

	#conn.write_channel('\r\n')

	# try to activate the device
	for _ in range(3):
		conn.write_channel('\r\n')
		sleep(0.4)

	node_def = node.node_definition
	device_type = None
	if node_def == 'iosv' or node_def == 'iosvl2':
		device_type = 'cisco_ios'
	elif node_def == 'asav':
		device_type = 'cisco_asa'
	else:
		print(f"Unrecognized node_definition: {repr(node_def)}, defaulting to 'cisco_ios' netmiko device_type", file=sys.stderr)
		device_type = 'cisco_ios'
	
	# tell netmiko what our actual device is
	netmiko.redispatch(conn, device_type)

	conn.write_channel('\r\n\r\n')
	#conn.write_channel('\r\n')
	sleep(0.5)
	conn.write_channel('\r\n\r\n')

	conn.find_prompt()

	conn.disable_paging()

	return conn





