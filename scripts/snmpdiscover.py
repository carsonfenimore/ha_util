#!/bin/python
import subprocess
import re

snmpAttributes = ["community", "auth_level", "auth_key", "priv_key", "version", "username", "priv_protocol", "auth_protocol" ]

def flexGet(obj, key):
    # Accepts dict or obj, returning value of attr, or None if not present
    if type(obj) == dict:
        if key in obj:
            return obj[key]
    else:
        return getattr(obj, key, None)

def snmpLookup(host, hostAttributes, searchoid, search, baseoid):
    # hostAttributes can be an obj, or dict, containing the members of switchMap below
    switchMap = {"community":"c",
                 "auth_level":"l", # authPriv, noAuthNoPriv, etc...
                 "auth_key": "A",
                 "auth_protocol": "a",
                 "priv_key": "X",
                 "priv_protocol":"x",
                 "username": "u",
                 "version": "v"}
    cmd = ["/usr/bin/snmpwalk", "-On"]
    for att in snmpAttributes:
        if flexGet(hostAttributes, att):
            cmd.append(f"-{switchMap[att]}")
            val = str(flexGet(hostAttributes,att))
            cmd.append(val)
    cmd.append(host)
    cmd.append(searchoid)
    #print(" ".join(cmd))

    res = subprocess.check_output(cmd).decode("utf-8")
    for line in res.split("\n"):
        match = re.search("([0-9.]+) = ([^:]+): (.+)", line)
        if not match:
            continue
        #print(line)
        oid = match.group(1)
        oidtype = match.group(2)
        oidval = match.group(3)
        if oidval[0] == '"':
            oidval = oidval[1:-1] # strip quotes
        if oidval == search:
            lastoctet = oid.split(".")[-1]
            newoid = f"{baseoid}.{lastoctet}"
            #print(f"Found oid {oid}/{oidtype} -> {oidval}; new oid {newoid}")
            return newoid

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
                        description='Scan a host using on oid, looking for a value, then generate a new oid given a base oid')
    parser.add_argument('--searchoid',help='The oid that we walk searching for a certain value.', required=True)
    parser.add_argument('--search',help='The criteria to look for inside the results of searchoid', required=True)
    parser.add_argument('--baseoid',help='The oid base that is used when we find the match. Roughly the last number on the search oid is appended to this.', required=True)
    parser.add_argument('--host',help='The host to search.', required=True)
    parser.add_argument('--community',help='snmp community', required=True)
    parser.add_argument('--auth_key',help='snmpv3 auth key')
    parser.add_argument('--auth_level',help='snmpv3 auth level')
    parser.add_argument('--auth_protocol',help='snmpv3 auth proto')
    parser.add_argument('--priv_key',help='snmpv3 priv key')
    parser.add_argument('--priv_protocol',help='snmpv3 priv proto')
    parser.add_argument('--username',help='snmpv3 username')
    parser.add_argument('--version',help='snmp version')
    args = parser.parse_args()
    print(snmpLookup(args.host, args, args.searchoid, args.search, args.baseoid ))
