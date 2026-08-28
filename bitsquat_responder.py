#!/usr/bin/env python3
import logging
import logging.handlers
import os
import socket
import sys

from dnslib import A, DNSRecord, QTYPE, RR

from squat_config import squatted_domains, target_domain, srcip

logger = logging.getLogger('bitsquat_responder')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(name)s: %(message)s')
handler.formatter = formatter
logger.addHandler(handler)


def rewrite_name(qname):
    """Replace configured bitsquatted domains with the target domain."""
    fixed_name = qname
    for name in squatted_domains:
        fixed_name = fixed_name.lower().replace(name, target_domain)
    return fixed_name


def build_responses(message):
    """Build the original response and, when needed, a corrected response."""
    request = DNSRecord.parse(message)
    qname = str(request.questions[0].qname)
    fixed_name = rewrite_name(qname)

    original = request.reply()
    original.add_answer(RR(qname, QTYPE.A, rdata=A(srcip), ttl=60))

    corrected = None
    if fixed_name != qname:
        corrected = DNSRecord.parse(message).reply()
        corrected.add_answer(RR(fixed_name, QTYPE.A, rdata=A(srcip), ttl=60))
        corrected.questions = []

    return original, corrected, qname


def main():
    s = socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_DGRAM)
    message, address = s.recvfrom(8192)
    localaddr = s.getsockname()
    s.close()

    pid = os.fork()
    if pid:
        sys.exit(0)

    original, corrected, qname = build_responses(message)
    logger.debug("%s asked for address %s", address[0], qname)

    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s2.bind(localaddr)
    s2.connect(address)

    s2.send(original.pack())
    if corrected:
        s2.send(corrected.pack())

    s2.close()


if __name__ == "__main__":
    main()
