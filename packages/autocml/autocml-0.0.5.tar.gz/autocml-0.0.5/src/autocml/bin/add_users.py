#!/usr/bin/env python3

import io
from ipaddress import IPv4Interface
import os
from posix import O_EXCL
import sys
import csv
import json
import argparse
from collections import namedtuple
from typing import Dict, List, NamedTuple, Tuple, Optional
import virl2_client as virl
import virl2_client.models as virlty

import autocml

description=[
	"Adds new users to an existing CML instance according to a supplied CSV file. Does not affect existing users."
]

def optparser():
	parser = argparse.ArgumentParser(
		description='\n'.join(description),
		parents=[autocml.argparse.root_parser()]
	)

	parser.add_argument('-d', '--delete',
		dest='delete',
		action='store_true', 
		help="Delete the users specified within the csv, instead of adding them"
	)
	parser.add_argument('-t', '--template',
		dest='write_template',
		action='store_true',
		help="Writes a user template file to the specified csv file. The file must not already exist."
	)
	parser.add_argument('interface_csv',
		help='A comma-seperated-value file, containing rows of "Username", "Password", "Full Name", "Description", "Roles", "Groups" where the last two are a comma separated list'
	)

	return parser

headers = ["Username","Password","Full Name","Description","Roles","Groups"]
def template():
	template = [
		','.join(headers),
		'user1,plaintext password,User One,The first user,admin,admin_group',
		'user2,another_password,User Two,The second user,,"net378,net123"',
	]
	return '\r\n'.join(template) + '\r\n'

UserRecord = namedtuple('UserRecord', ['username', 'password', 'fullname', 'description', 'roles', 'groups'])

def main(pargs=None):
	parser = optparser()
	args = parser.parse_args(pargs)

	if args.write_template:
		with io.open(args.interface_csv, "x") as f:
			f.write(template())
		return 0

	client = autocml.get_client(args)

	# read in the file's entries
	users = []
	with io.open(args.interface_csv, 'r') as f:
		for li, entry in enumerate(csv.reader(f)):
			if li == 0:
				assert entry == headers, "Passed interface file is not a valid tab seperated user descriptor file"
			elif len(entry) == len(headers):
				#user, password, fullname, desc, rroles, rgroups = entry
				userrec = UserRecord(*entry)
				userrec = userrec._replace(
					roles = [ s.strip() for s in userrec.roles.split(',') ],
					groups = [ s.strip() for s in userrec.groups.split(',') ],
				)
				
				print(repr(userrec))

				users.append(userrec)
			elif len(entry) == 0:
				pass # ignore blank lines
			else:
				print(f"[lint][{args.interface_csv}:{li+1}] the entry `{repr(entry)}` does not have exactly {len(headers)} values ({','.join(headers)})", file=sys.stderr)

	cml_users = client.user_management.users()
	if args.delete:
		for user in users:
			if user.username in cml_users.keys():
				print(f"Deleting user {user.username}...")
				client.user_management.delete_user(user.username)
	else:
		for user in users:		
			if user.username not in cml_users.keys():
				print(f"Creating user {user.username}...")
				client.user_management.create_user(
					user.username, user.password,
					user.fullname,
					user.description,
					user.roles, user.groups
				)
			else:
				print(f"Skipping user {user.username} (already exists)")

if __name__ == "__main__":
	main()


