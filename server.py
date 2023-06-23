from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
from osc4py3 import oscbuildparse

def handler(address, s, x, y):
    # Will receive message address, and message data flattened in s, x, y
    print(address, s, x, y)

# Start the system.
osc_startup()

# Make server channels to receive packets.
osc_udp_server("192.168.56.1", 11001, "tov_server")
# osc_udp_client("192.168.56.1", 11000, "tov_client")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/live/*", handler, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)

# msg = oscbuildparse.OSCMessage("/live/test", ",sif", ["text", 672, 8.871])
# osc_send(msg, "tov_client")

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    osc_process()

# Properly close the system.
osc_terminate()