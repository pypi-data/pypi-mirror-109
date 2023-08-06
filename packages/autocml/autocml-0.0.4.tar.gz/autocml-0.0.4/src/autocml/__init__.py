
#from .auth import *
#from .connections import *
#from .parallel import *
#from . import bin

import re
from typing import List, Optional

import virl2_client as virl
import virl2_client.models as virl_ty

#__all__ = ['interface_matches', 'interface_best_match', 'auth', 'connections', 'parallel', 'bin']
from .auth import get_client
from .connections import resolve_lab, connect_to_device
from .parallel import for_all
from .argparse import root_parser as argarse_client
from . import bin
from . import argparse

intnumreg = re.compile("(\d+/)*\d+$")

def interface_matches(ios: str, user: str) -> bool:
	""" Returns true if the `user` interface is a possible match for the `ios` interface """
	ios = ios.upper()
	usr = user.upper()
	# try matching based on last numbers + if non-zero start matches?
	# assume users are using non-conflicting interfaces
	ios_lower, ios_upper = intnumreg.search(ios).span()
	usr_lower, usr_upper = intnumreg.search(usr).span()

	ios_num = ios[ios_lower:ios_upper]
	usr_num = usr[usr_lower:usr_upper]

	if ios_num != usr_num:
		return False

	return ios.startswith(usr[:usr_lower])

assert interface_matches("GigabitEthernet0/0", "G0/0")
assert interface_matches("Loopback0", "L0")
assert interface_matches("FastEthernet0/23", "Fa0/23")
assert not interface_matches("FastEthernet0/23", "Fe0/23")

def interface_best_match(ios: List[str], user: str) -> Optional[str]:
	matching = [ref for ref in ios if interface_matches(ref, user)]
	matching.sort(key=lambda e: len(e), reverse=True)
	
	return None if len(matching) == 0 else matching[0]

def custom_endpoint_get(client: virl.ClientLibrary, url: str, json: bool=True):
	""" Performs an authenticated GET request against the CML controller. The url should not contain a leading slash. Output will be JSON'ified unless json=False has been passed """

	r=client.session.get(client._base_url + url)
	
	r.raise_for_status()

	if json:
		return r.json()
	else:
		return r.text
