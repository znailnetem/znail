import flask

from znail.netem.tcpdump import TcpDump
from znail.ui import app


@app.route("/capture.pcap")
def capture():
    with TcpDump("eth1") as generator:
        return flask.Response(generator, content_type="application/vnd.tcpdump.pcap"), 200
