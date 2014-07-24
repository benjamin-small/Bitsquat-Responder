Bitsquat-Responder
==================

A quick DNS server to respond to bitsquatted domain requests

The code should be called by xinet.d. An example config is:

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

Values in the squat_config.py file should be updated to reflect the IP and domains you're squatting.

### Requires

* dnslib
* xinet.d

