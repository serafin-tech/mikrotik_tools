# helper scripts for configuring Mikrotik routers

## dhcp_options.py

```
usage: dhcp_options.py [-h] [-v] {unifi_43,classless_routes} ...

Script to generate MikroTik DHCP options

positional arguments:
  {unifi_43,classless_routes}
    unifi_43            Option 43 for Unifi Controller address
    classless_routes    Option 121 for classless static routes

options:
  -h, --help            show this help message and exit
  -v, --verbose         talkative mode
```

## hosts_definition.py

```
usage: hosts_definition.py [-h] [-v] -f FILE [-o OUTPUT] -t {dns,dhcp}

Script to generate hosts definition for Mikrotik router

options:
  -h, --help            show this help message and exit
  -v, --verbose         talkative mode
  -f FILE, --file FILE  xlsx file with hosts definition
  -o OUTPUT, --output OUTPUT
                        output file
  -t {dns,dhcp}, --output-type {dns,dhcp}
                        type of output, to be selected from ['dns', 'dhcp']
```