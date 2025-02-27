import subprocess
import re

def snmpLookup(host, searchoid, search, baseoid):
    cmd = ["/usr/bin/snmpwalk",
        "-v2c", "-c", "public","-On",host, searchoid]
    res = subprocess.check_output(cmd).decode("utf-8")
    for line in res.split("\n"):
        match = re.search("([0-9.]+) = (.+): (.+)", line)
        if not match:
            continue
        oid = match.group(1)
        oidtype = match.group(2)
        oidval = match.group(3)
        if oidtype == "STRING":
            oidval = oidval[1:-1]
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
    args = parser.parse_args()
    snmpLookup(args.host, args.searchoid, args.search, args.baseoid)
