#!/usr/bin/env python3

import io
import os
import sys
from typing import List, Union
import argparse
import base64
from requests import HTTPError
import yaml
import virl2_client as virl
from virl2_client.virl2_client import Version
import autocml

description=[
	"Uploads or downloads YAML Labs from the CML controller.",
	"Note that downloading only affects the currently saved YAML files.",
	"You may first want to extract the configurations for running labs.",
]

def optparser():
	parser = argparse.ArgumentParser(
		description='\n'.join(description),
		parents=[autocml.argparse.root_parser()]
	)
	parser.add_argument('-u', '--user',
		dest="user",
		help="[admin only] Operate on a specific user's labs. Takes precedence over --all"
	)
	# parser.add_argument('-t', '--test',
	# 	dest='test_args',
	# 	action='store_true',
	# 	help="Print a debug representation of these parsed arguments",
	# )

	subcmds = parser.add_subparsers(
		dest='action',
		help="Actions:",
		required=True,
	)
	
	
	subcmd_download = subcmds.add_parser('download', help="Download some or all of the user lab YAMLs")
	subcmd_download.add_argument('-a', '--all',
		dest='dump_all',
		action='store_true',
		help="[admin only] Operate on all the controller's labs."
	)
	subcmd_download.add_argument('-r', '--running',
		dest='allow_running',
		action='store_true',
		help="Allow download even if a lab is running (downloaded .yaml may be stale)"
	)
	subcmd_download.add_argument('folder', help='The directory to put YAML files into.')



	subcmd_upload = subcmds.add_parser('upload', help="Upload YAML labs from disk to the CML controller")
	subcmd_upload.add_argument('-o', '--overwrite',
		dest='overwrite',
		action='store_true',
		help="Overwrite existing labs on the controller by the same title. Labs must be stopped/wiped."
	)
	subcmd_upload.add_argument('-i', '--ignore',
		dest='ignore',
		action='store_true',
		help="Ignore existing labs on the controller by the same title. Will create labs with duplicate titles."
	)
	subcmd_upload.add_argument('-s', '--skip',
		dest='skip',
		action='store_true',
		help="Skips existing labs on the controller by the same title. Will not upload labs with duplicate titles."
	)
	subcmd_upload.add_argument('folder', help='The directory to read YAML files from.')
	


	subcmd_delete = subcmds.add_parser('delete', help="Bulk delete some or all of the user labs on the CML controller")
	subcmd_delete.add_argument('-a', '--all',
		dest='dump_all',
		action='store_true',
		help="[admin only] Operate on all the controller's labs."
	)
	subcmd_delete.add_argument('-y', '--yes',
		dest='confirmed',
		action='store_true',
		help="Do not prompt for user confirmation for lab deletion."
	)
	subcmd_delete.add_argument('-f', '--force',
		dest='force',
		action='store_true',
		help="If necessary, shuts down labs so they can be deleted."
	)

	return parser

def download(
	client: virl.ClientLibrary,
	folder: str,
	users: Union[bool, str] = False,
	allow_running: bool = False,
):
	"""
	Downloads YAML files from the controller to disk.
	
	If `allow_running` is `False`, then this function exists early if any labs are running.
	
	Arguments:
		`client` (`virl2_client.ClientLibrary`): An authenticated client library for the CML controller.
		`folder` (`str`): The output folder for each lab YAML. Labs are named after their title.
		`allow_running` (`bool=False`): If true, then labs are allowed to run.
		`users` (`bool=False`): True if the function should download all the current user's labs. If true, each users' labs will be downloaded to their own folders.
		`users` (`str`): A specific user on the controller to download their labs.
	"""

	if os.path.isdir(folder) and len(os.listdir(folder)) != 0:
		print("Destination folder is not empty. Choose another folder, or empty it", file=sys.stderr)
		return 1

	labs: List[virl.virl2_client.Lab] = client.all_labs(show_all=(users != False))

	#if not allow_running:
	found_active=False
	for lab in labs:
		if lab.is_active():
			status='error' if not allow_running else 'warn'
			print(f'[{status}] lab is {lab.state()}: {lab.id}/{lab.title}', file=sys.stderr)
			found_active=True
	if found_active and not allow_running:
		print('', file=sys.stderr)
		print('Found active labs. Please stop them before extracting labs, or pass --running to continue and retrieve the latest extracted configurations', file=sys.stderr)
		return 2

	for lab in labs:
		if isinstance(users, str):
			if lab.owner != users:
				continue
		
		# destination folder, lab yaml
		fname = lab.id + '.yaml'
		if users == True: # show_all
			# insert the lab owner's name as a filename prefix, if necessary
			fname = lab.owner + '.' + fname
	
		filename = os.path.join(folder, fname)
		print(f"downloading lab to {filename} -- {lab.title}")
		lab_yaml = lab.download()

		try:
			os.makedirs(folder, exist_ok=True)
			with io.open(filename, "w") as f:
				f.write(lab_yaml)
		except OSError as e:
			ownerclause = ' (owner: ' + lab.owner + ')' if users == True else ''
			print(f"[error] Unable to write lab {lab.id}/{lab.title}{ownerclause} to disk due to a system error. Try renaming the lab on the controller?", file=sys.stderr)
			print(e, file=sys.stderr)

def delete(client: virl.ClientLibrary,
	users: Union[bool, str] = False,
	confirmed: bool = False,
	force: bool = False,
):
	from ..bin import query_yes_no

	labs: List[virl.virl2_client.Lab] = client.all_labs(show_all=(users != False))
	
	if not confirmed:
		user_string=None
		if users == True:
			user_string = "ALL"
		else:
			user = client.username if users == False else users
			user_string = user + "'s"
		
		result = query_yes_no(f"Are you sure you want to delete {user_string} labs from the controller?", default="no")
		if not result:
			return 3

	for lab in labs:
		if isinstance(users, str):
			if lab.owner != users:
				continue
		
		print(f"[{lab.owner}] Removing lab {lab.id} ({lab.title})")
		if force:
			lab.stop(wait=True)
			lab.wipe(wait=True)
			lab.remove()
		else:
			try:
				lab.remove()
			except HTTPError as e:
				print("[error] deleting lab, may not be stopped or wiped. ignoring.", file=sys.stderr)

def upload(client: virl.ClientLibrary,
	folder: str,
	user: str = None,
	overwrite: bool = False,
	ignore: bool = False,
	skip: bool = False,
):

	dirents = list(ent for ent in os.scandir(folder) if ent.name.endswith('.yaml') and ent.is_file())
	by_user = dict()

	# read files from disk, sort by title
	for ent in dirents:
		with io.open(ent.path, 'r') as f:
			lab_yaml = f.read()
		parsed = yaml.full_load(lab_yaml)
		title = parsed['lab']['title']

		as_split = ent.name.split('.')
		if len(as_split) == 2:
			user = user if user is not None else client.username
		elif len(as_split) == 3:
			user = as_split[0]
		else:
			raise RuntimeError(f"unexpected lab yaml filename: {ent.name} (expected $id.yaml or $user.$id.yaml)")

		by_title = by_user.setdefault(user, dict())

		titleent = by_title.setdefault(title, list())
		titleent.append(lab_yaml)

	for owner, by_title in by_user.items():
		if owner != client.username:
			print(f"The VIRL library does not enable us to upload labs on behalf of other users, even as admin. Therefore, {owner} will have to upload their own labs.", file=sys.stderr)
			continue

		for title, labs in sorted(by_title.items()):
			if not ignore:
				existing_labs = client.find_labs_by_title(title)
				if len(existing_labs) > 0:
					if skip:
						continue
					elif overwrite:
						for lab in existing_labs:
							lab.stop()
							lab.wipe()
							lab.remove()

			for lab_yaml in labs:
				topo = lab_yaml
				print(f"[{owner}] Uploading {title}")
				uploaded = client.import_lab(topo, 'tmp-title')
				uploaded.title = title

def main(pargs=None):
	parser = optparser()
	args = parser.parse_args(pargs)

	# if args.test_args:
	# 	print(args)
	# 	return 1

	client = autocml.get_client(args)

	if args.user is not None and args.user != client.username:
		# I do not personally have admin access to a multi-user instance to test this
		# I think the code is built to allow this already, it would just need to be tested/verified
		raise NotImplementedError("specifying a specific user is not yet implemented")

	if args.action == 'download' or args.action == 'delete':
		targets = args.dump_all
		if args.user is not None:
			targets = args.user

	if args.action == 'download':
		return download(client, args.folder, users=targets, allow_running=args.allow_running)
	elif args.action == "upload":
		return upload(client, args.folder, user=args.user, overwrite=args.overwrite, ignore=args.ignore, skip=args.skip)
	elif args.action == "delete":
		return delete(client, users=targets, confirmed=args.confirmed, force=args.force)
	else: # should not be reachable - argparse should mandate the action, and validate it
		raise ValueError("unrecognized command line action - this is a programmer error")
	
if __name__ == "__main__":
	main()


