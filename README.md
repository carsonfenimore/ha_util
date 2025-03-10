# Home Assistant Utilities
More compact home assistant snmp yaml - also supports oid lookup of snmp tables

## ha_snmp_gen.py
Normally if you want to pull in snmp oids, HA requires you to repeat the host and creds for each oid. This creates a bit of a maintenance problem.  Additionally it requires tedious repetitiion of configuration - sometimes up to 16 lines of yaml per oid.  With this tool each oid takes about 2 lines of yaml.  Here is a sample:

```yaml
snmp:
- host: 10.10.2.2
  version: '3'
  auth_level: authPriv
  auth_key: authpassword
  auth_protocol: SHA
  priv_key: privpassword
  priv_protocol: DES
  username: user
  items:
  - qnap_public_share_x:
      oid: .1.3.6.1.2.1.25.2.3.1.3.37
  - qnap_fendocs_x:
      oid: 1.3.6.1.2.1.25.2.3.1.6
      search_oid: 1.3.6.1.2.1.25.2.3.1.3
      search_value: "/share/NFSv=4/FenDocs2"
```

In the example above two oids are provided.  The first oid showcases how the simple configuration requires only two lines per oid - one for the oid name, another for the oid.  

The second oid in this example is a table lookup - see below for more details.
id 


### snmp table lookups
When a search_oid nd search_value item is provided, the script performs an snmpwalk looking for an oid whose value matches.  If found the last octet of the matching oid is used to form a new oid, based on the "oid" param. This is then used as the oid for generating the ha yaml.

### Allowed params
For each item we support nearly every param from the snmp page: unit_of_measurement, value_template, accept_errors, default_value, etc.  

For the host we support v1/2c/3 - however for v3 we only support des as the priv_protocol, and sha as the auth_protocol.  

### Using
Make a "sensors" folder in your ha configuration directory.  

In your HA config include a list of sensor yamls as follows:

```yaml
sensor: !include_dir_merge_list sensors/
```

Now run the utility:

```python
python ha_snmp_gen.py --infile snmp_input.yaml --outfile <haconfig>/sensors/snmp.yaml
```

And restart HA and you should see the new sensors.
