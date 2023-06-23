# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

import time

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("192.168.56.1", 11000, "aclientname")

# Build a simple message and send it.
msg = oscbuildparse.OSCMessage("/live/test", ",sif", ["text", 672, 8.871])
osc_send(msg, "aclientname")


# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # You can send OSC messages from your event loop too…
    # …
    osc_process()
    # …

# Properly close the system.
osc_terminate()