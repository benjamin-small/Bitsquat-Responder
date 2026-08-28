# Testing

Run the test suite and measure coverage with:

```sh
python -m pip install -r requirements-dev.txt
python -m coverage run --source=bitsquat_responder -m unittest discover -s tests -v
python -m coverage report
```

The tests cover configured domain rewriting and DNS response construction for ordinary and bitsquatted queries. They do not open a live UDP socket, fork a process, exercise xinetd, or verify syslog integration.

The current measured statement coverage is **64% (32 of 50 statements)**. It was measured with Coverage.py 7.10.6 using the command above.
