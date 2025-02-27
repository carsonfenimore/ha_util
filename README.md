# Home Assistant Utilities
A few things to make HA configuration easier

## ha_snmp_gen.py
Normally if you want to pull in snmp oids, HA requires you to repeat the host and creds for each oid. To avoid this duplication of data, we introduce a more compact yaml format.  Here is a sample:

```yaml
snmp:
- host: 10.10.2.2
  community: public
  items:
  - qnap_public_share:
      oid: .1.3.6.1.2.1.25.2.3.1.3.37
  - qnap_fendocs_share:
      oid: 1.3.6.1.2.1.25.2.3.1.6
      search_oid: 1.3.6.1.2.1.25.2.3.1.3
      search_value: "/share/NFSv=4/FenDocs2"
```

Note that for each oid one need only specify the name and oid.  


### snmp table lookups
In the example above one of the oids specifies a search_oid and search_value.  This uses snmp table logic to lookup the given value under the search oid.  Once found the last octet of the corresponding oid is used to form a new oid, based on the oid param. This is then used as the oid for generating the ha yaml.

### Using
To use ensure there is a line in your ha config such as:

```yaml
sensor: !include_dir_merge_list sensors/
```

Ensure there is a "sensors" folder inside your ha configuration directory.  Then run:

```python
python ha_snmp_gen.py --configuration snmp_input.yaml --outfile <haconfig>/sensors/snmp.yaml
```

And restart HA and you should see the new sensors.
