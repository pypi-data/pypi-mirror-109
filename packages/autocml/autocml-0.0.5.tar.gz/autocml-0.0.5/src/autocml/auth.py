
import argparse
import sys
import os
import base64
import ssl
from typing import Tuple

try:
	import virl2_client as virl
except ImportError:
	print("Unable to load CML client library.")
	CML_HOST="$CML_HOST"
	if "CML_HOST" in os.environ:
		CML_HOST = os.environ["CML_HOST"]
	print(f"Please install using the wheel from https://{CML_HOST}/client")
	print("then:")
	print("pip3 install <downloaded virl2_client-version.whl>")
	exit(1)



def from_env(exit_on_missing=True) -> Tuple[str, str, str]:
	""" Retrieves the CML authentication info from the environment and returns it as (host, user, passwd) """
	env = os.environ
	host = (env.get("CML_HOST"), env.get("VIRL2_URL"), env.get("BREAKOUT_CONTROLLER"))
	user = (env.get("CML_USER"), env.get("VIRL2_USER"), env.get("BREAKOUT_USERNAME"))
	pass64 = env.get("CML_PASS64")
	passwd = (env.get("CML_PASS"), env.get("VIRL2_PASS"), env.get("BREAKOUT_PASSWORD"))
	
	rtn_host = next(h for h in host if h is not None)
	rtn_user = next(u for u in user if u is not None)
	if pass64 is not None:
		rtn_pass = base64.b64decode(pass64).decode("utf-8")
	else:
		rtn_pass = next(p for p in passwd if p is not None)

	# ensure all are populated
	if exit_on_missing and not all([rtn_host, rtn_user, rtn_pass]):
		print("Not all host environment variables present. Must have:", file=sys.stderr)
		print("CML_HOST or VIRL2_URL or BREAKOUT_CONTROLLER: CML host IP/address")
		print("CML_USER or VIRL2_USER or BREAKOUT_USERNAME: The username of the CML user")
		print("CML_PASS64 or CML_PASS or VIRL2_PASS or BREAKOUT_PASSWORD: The password of the CML user (where CML_PASS64 is in base64 format)")
		exit(1)

	return (rtn_host, rtn_user, rtn_pass)

def client_from_env(ssl_verify: bool=False, exit_on_error: bool=True) -> virl.ClientLibrary:
	import requests
	
	host, user, passwd = from_env()
	try:
		return virl.ClientLibrary(host, user, passwd, ssl_verify=ssl_verify)
	except requests.exceptions.SSLError as e:
		if 'certificate verify failed' in str(e):
			print("Certificate verification failed. Self-signed certificate? Try passing --nosslverify or adding the controller's certificate to your local certificate store.", file=sys.stderr)
			if exit_on_error:
				exit(1)
			return None
		else:
			raise e

def get_client(ns: argparse.Namespace = None, ssl_verify: bool = None, exit_on_error: bool = None) -> virl.ClientLibrary:
	"""
	Searches for environment variables suitable for creating a `virl.ClientLibrary`
	
	An `argparse.Namespace` can be passed to provide configurations. The namespace keys are defined in `autocml.argparse_client`

	If exit_on_error is None/not passed, then it will be true for scripts and false for interactive sessions.
	"""

	ssl_verify=ssl_verify

	if exit_on_error is None:
		try:
			import __main__ as main
			exit_on_error = hasattr(main, '__file__')
		except:
			exit_on_error = True

	if ssl_verify is None and ns is not None:
		try:
			ssl_verify = not ns.nosslverify
		except AttributeError:
			raise ValueError("argparse Namespace does not have an `nosslverify` attribute - did it come from `autocml.argparse_client` ?")
	elif ssl_verify is None and ns is None:
		ssl_verify=True
	
	return client_from_env(ssl_verify=ssl_verify, exit_on_error=exit_on_error)



