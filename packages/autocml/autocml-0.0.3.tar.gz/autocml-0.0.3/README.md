# AutoCML

# Authentication
This library (and associated scripts) supports authentication via environment variables. This library supports a variety of different variable names, meant to suit the different names Cisco already uses.

|Purpose|This Library|VIRL Library|Breakout Tool|Example|
|--|--|--|--|--|
|CML Controller|`CML_HOST`|`VIRL2_URL`|`BREAKOUT_CONTROLLER`|`192.168.0.50`|
|Username|`CML_USER`|`VIRL2_USER`|`BREAKOUT_USERNAME`|`admin`|
|Password (Base-64)|`CML_PASS64`|||`cGFzc3dvcmQ=`|
|Password|`CML_PASS`|`VIRL2_PASS`|`BREAKOUT_PASSWORD`|`password`|


Any combination of the above variables can be used, although the leftmost variable name will be prioritized in case of conflicts. Using `CML_PASS64` is recommended (and prioritized over other password variables) to prevent the likelyhood of successful shoulder-surfers.

## Bash example
```sh
CML_HOST="<cml server hostname/IP address>"
CML_USER="admin"
CML_PASS="password"
```
Note: Above example uses a plaintext password. I first recommend converting it to base64, then passing it in a `CML_PASS64` environment variable.

# Installing

The following should work in both Linux/Bash, and PowerShell.
```sh
pip install virl2-client # Install official VIRL/CML library from Cisco
pip install autocml # Install this library + associated utilities
```

# Scripts

This library includes common scripts/commands useful for administrative purposes, or for automating common lab scenarios.

## cml-add-users

Loads in a CSV file containing a list of users (a sample CSV can be saved by running `cml-add-users --template <OUTPUT TEMPLATE FILENAME>`

By default, it adds the users in the csv file to the authenticated CML instance. It only adds/affects users that do not already exist.

Can also delete users that are listed in the csv, if a `--delete` flag is passed.

Example template:
```csv
Username,Password,Full Name,Description,Roles,Groups
user1,plaintext password,User One,The first user,admin,admin_group
user2,another_password,User Two,The second user,,"net378,net123"
```

Example usage: `cml-add-users <USER CSV FILENAME>`

View help info for more details (`cml-add-users --help`)

(Currently untested as the primary author does not have admin access to a multi-user instance)

## cml-verify-ints

Asserts a lab's interfaces against a .csv file. The csv file must have exactly three columns, (device ID/label, interface, and IP address (with optional CIDR notation)) and may look like the following:

```csv
Node Label,Int,IPv4
n0,GigabitEthernet0/0,192.168.0.24/26
R2,Fa0/2,10.1.34.2/24
R3,L1,10.255.0.3/32
```

One ran, it will print a report showing which interfaces match, or do not match. Interfaces not listed will not be checked.

Can also dump a CSV of interfaces, that can later be used with this utility to double-check interface addresses.

Also has a flag to emit results as JSON, although it cannot read in JSON inputs.

## cml-bulk-labs

Allows for downloading/uploading/deleting lab YAMLs in bulk for archival purposes. Useful when migrating YAML labs files from one CML controller to another (like for a fresh upgrade).

View the help for detailed configuration options/features (`cml-bulk-labs --help`)

## cml-dump-cfgs (WIP)

## cml-dump-cmds (WIP)

## cml-dump-pings (WIP)

## cml-pcap (WIP)

## cml-start-session (WIP)

Opens a tabbed terminal emulator to have a tab for each node's console within a lab.
