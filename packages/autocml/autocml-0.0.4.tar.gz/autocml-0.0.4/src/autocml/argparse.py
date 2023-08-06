
import argparse

def root_parser() -> argparse.ArgumentParser:
	"""
	Returns an instance of `argparse.ArgumentParser` that is capable of creating a CML Client

	The namespace produced by parsing arguments can be used in `autocml.get_client()`
	"""
	parser = argparse.ArgumentParser(add_help=False)

	parser.set_defaults(
		nosslverify=False,
	)

	parser.add_argument('-s', '--nosslverify',
		dest='nosslverify',
		action='store_true',
		help="Do not verify the server's TLS certificate",
	)

	return parser

def add_lab_desc(ap: argparse.ArgumentParser):
	ap.add_argument('-u', '--user',
		dest="user",
		help="[admin only] Operate on a different user's lab."
	)

	ap.add_argument('lab_description',
		help="The ID or title of the lab. Start of the ID/title can be used if enough characters exist to disambiguate it. ID preferred for exact match, title preferred for partial match."
	)
