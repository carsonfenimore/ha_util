#!/bin/python
import argparse
import sys
import yaml
from snmpdiscover import snmpLookup
from snmpdiscover import snmpAttributes


def extractAttributes(params, attributes):
    out = ""
    for att in attributes:
        if att == 'auth_level':
            continue
        if att in params:
            val = params[att]
            if "protocol" in att:
                val = val.lower()
                if val == 'sha':
                    val = 'hmac-sha'
            val = f"'{val}'"
            out += f"  {att}: {val}\n"
    return out

def run(infile, outfile=None):
    itemAttributes = ["unit_of_measurement", "value_template", "accept_errors", "default_value" ]

    outf = sys.stdout
    if outfile:
        outf = open(outfile,"w") 

    with open(infile, "r") as inf:
        yamlFile = yaml.safe_load(inf)

    for host in yamlFile['snmp']:
        hostname = host['host']
        for item in host['items']:
            for name, params in item.items():
                if "search_oid" in params and "search_value" in params:
                    oid = snmpLookup(hostname, host, params['search_oid'], params['search_value'], params['oid'])
                else:
                    oid = params['oid']
                #print(f"\t{name:}, oid: {oid}")
                outs = f"""
- platform: snmp
  host: {hostname}
  baseoid: {oid}
  unique_id: {name}
  name: {name}
"""
                outs = outs + extractAttributes(params, itemAttributes)
                outs = outs + extractAttributes(host, snmpAttributes)
                outf.write(outs)
    outf.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        description='Generate sensor yaml for HA given a compact list of oids - supports table lookup too!')
    parser.add_argument('--infile',help='File containing simplified HA snmp sensors', required=True)
    parser.add_argument('--outfile',help='If not provided, standard out is used')
    args = parser.parse_args()

    run(args.infile, args.outfile)



