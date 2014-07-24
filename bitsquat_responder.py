#!/usr/bin/env python
from dnslib import *
from squat_config import squatted_domains, target_domain, srcip
import socket, time, sys, os
import logging, logging.handlers

logger = logging.getLogger('bitsquat_responder')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(name)s: %(message)s')
handler.formatter = formatter
logger.addHandler(handler)

s = socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_DGRAM)
message, address = s.recvfrom(8192)
localaddr = s.getsockname()
s.close()

pid = os.fork()
if pid:
    sys.exit(0)


r = DNSRecord.parse(message)

qname = str(r.questions[0].qname)
fixed_name = qname

for name in squatted_domains:
	fixed_name = fixed_name.lower().replace(name, target_domain)

a = r.reply()
a.add_answer(RR(qname,QTYPE.A,rdata=A(srcip),ttl=60))

b = None

if fixed_name != qname:
	r2 = DNSRecord.parse(message)
	b = r2.reply()
	b.add_answer(RR(fixed_name,QTYPE.A,rdata=A(srcip),ttl=60))
	b.questions = []

logger.debug("%s asked for address %s" % (address[0], qname))

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind(localaddr)
s2.connect(address)

s2.send(a.pack())
if b:
	s2.send(b.pack())

s2.close()
