import argparse
import yaml
from snmpdiscover import snmpLookup

parser = argparse.ArgumentParser(
                    description='Generate sensor yaml for HA given a compact list of oids - supports table lookup too!')
parser.add_argument('--configuration',help='yaml filename containing list of oids', required=True)
parser.add_argument('--outfile',help='Where to output', required=True)
args = parser.parse_args()

with open(args.outfile,"w") as outf:
    with open(args.configuration, "r") as inf:
        yamlFile = yaml.safe_load(inf)
    for host in yamlFile['snmp']:
        hostname = host['host']
        community = host['community']
        #print(f"Host: {hostname}, community: {community}")
        for item in host['items']:
            for name, params in item.items():
                if "search_oid" in params and "search_value" in params:
                    oid = snmpLookup(hostname, params['search_oid'], params['search_value'], params['oid'])
                else:
                    oid = params['oid']
                #print(f"\t{name:}, oid: {oid}")
                outf.write(f"""
- platform: snmp
  host: {hostname}
  community: {community}
  baseoid: {oid}
  unique_id: {name}
  name: {name}
""")
