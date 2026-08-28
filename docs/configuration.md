# Configuration

Edit `squat_config.py` before deploying the responder:

- `target_domain` is the canonical domain used in the additional corrected DNS response.
- `srcip` is the IPv4 address returned in DNS A records.
- `squatted_domains` lists domain spellings that should be rewritten to `target_domain`.

The process does not read environment variables. It expects xinetd to pass a UDP socket on standard input, as shown in the README, and it sends logs to `/dev/log` through syslog.
