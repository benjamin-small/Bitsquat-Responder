Bitsquat-Responder
==================

Bitsquat-Responder is a small UDP DNS service that identifies configured bitsquatted domain requests, returns the configured address, and sends an additional response for the corrected domain name.

It supports Python 3.11 or newer and requires `dnslib` plus an xinetd-compatible host.

## Setup and usage

Install the runtime dependency and configure the domain mappings:

```sh
python3 -m pip install -r requirements.txt
$EDITOR squat_config.py
```

The program is intended to be called by xinetd. An example configuration is:

		root@localhost:~# cat /etc/xinetd.d/bitsquat_responder 
		# default: on 
		# description: a service to respond to dns requests 
		# This is the udp version.
		service domain 
		{
				disable         = no
				port            = 53 
				socket_type     = dgram
				protocol        = udp
				user            = root
				wait            = yes
				server      = /root/bitsquat_responder/bitsquat_responder.py
		}

Update `squat_config.py` to reflect the returned IP address, canonical domain, and domains you are monitoring. See [configuration documentation](docs/configuration.md) for every setting.

## Testing

The automated tests exercise domain rewriting and DNS packet construction. See [testing documentation](docs/testing.md) for commands, measured coverage, and the explicitly excluded system integrations.

## Licensing

See [licensing documentation](docs/licensing.md) for the repository's current license status.
