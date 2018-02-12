"""
Provides network emulation (netem) facilities.

This package translates the desired network emulation state into calls to the
appropriate command line tools, such as "tc" or "iptables". Given that these
tools require administrative privileges for most operations, this package assume
that it is running in a Python interpreter with such privileges.
"""
