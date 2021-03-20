from collections import OrderedDict

import flask
import requests

from znail import __version__
from znail.ui import app
from znail.update import is_update_available

delay_examples = [
    {
        "description": "The average delay of a transatlantic connection",
        "value": 100,
    },
    {
        "description": "The average delay of a connection within the EU or the US",
        "value": 35,
    },
    {
        "description": "A satellite modem in the woods (terrible!)",
        "value": 600,
    },
]

loss_examples = [
    {
        "description": "A wifi connection on the same channel as all your neighbours in an densely populated apartment building",
        "value": "10",
    },
    {
        "description": "Packet loss high enough for streamed video/voip to have problems",
        "value": "7.5",
    },
    {
        "description": "A fairly high packet loss rate under which things should still work.",
        "value": "2.5",
    },
]

duplication_examples = [
    {
        "description": "Two switches misconfigured to broadcast the same traffic to the same address ",
        "value": "100",
    },
    {
        "description": "Duplication due to high packet loss causing dropped ACKs",
        "value": "5",
    },
    {
        "description": "Duplication due to minor packet loss causing dropped ACKs",
        "value": "2",
    },
]

reordering_examples = [
    {
        "description": "Some packets taking a slower path through the network",
        "ms": 100,
        "percent": "5",
    },
    {
        "description": "Many packets taking an almost as good path through the network",
        "ms": 10,
        "percent": "50",
    },
]

corruption_examples = [
    {
        "description": "DSL Modem with degrading filter",
        "value": "1",
    },
    {"description": "Poorly shielded cable next to an EMI source", "value": "5"},
]

rate_examples = [
    {
        "description": "A dialup modem",
        "kbit": 56,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "A slow ADSL connection",
        "kbit": 1536,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "A standard ADSL connection",
        "kbit": 4096,
        "latency": 1000,
        "burst": 10000,
    },
    {
        "description": "The max throughput of udp over 802.11b wifi",
        "kbit": 7270,
        "latency": 1000,
        "burst": 10000,
    },
]


def _api_url(path):
    return "{host_url}api{path}".format(host_url=flask.request.host_url, path=path)


@app.route("/")
def index():
    def _get_status(url, json_parameter=None):
        response = requests.get(_api_url(url), timeout=2)
        if json_parameter:
            return bool(response.json()[json_parameter])
        return bool(response.json())

    packet_control_summary = OrderedDict(
        [
            ("Packet Delay", _get_status("/disciplines/packet_delay", "milliseconds")),
            ("Packet Loss", _get_status("/disciplines/packet_loss", "percent")),
            ("Packet Duplication", _get_status("/disciplines/packet_duplication", "percent")),
            ("Packet Reordering", _get_status("/disciplines/packet_reordering", "percent")),
            ("Packet Corruption", _get_status("/disciplines/packet_corruption", "percent")),
            ("Packet Rate Control", _get_status("/disciplines/packet_rate_control", "kbit")),
        ]
    )
    network_control_summary = OrderedDict(
        [
            ("Disconnect", _get_status("/disconnect", "disconnect")),
            ("Whitelist", _get_status("/whitelist")),
            ("DNS Override", _get_status("/dnsoverride")),
            ("IP Redirect", _get_status("/ipredirect")),
        ]
    )

    return _render_template(
        "index.html",
        current_page="overview",
        packet_control_summary=packet_control_summary,
        network_control_summary=network_control_summary,
    )


@app.route("/health")
def health():
    health_check_results = requests.get(_api_url("/healthcheck"), timeout=2).json()
    return _render_template(
        "health.html",
        current_page="health",
        health_check_results=health_check_results,
        system_is_healthy=all(health_check_results.values()),
    )


@app.route("/about")
def about():
    return _render_template("about.html", current_page="about")


@app.route("/packet_delay", methods=["GET", "POST"])
def get_packet_delay():
    endpoint = _api_url("/disciplines/packet_delay")
    clear_endpoint = _api_url("/disciplines/packet_delay/clear")
    success = True
    message = None
    milliseconds = None
    examples = delay_examples

    if flask.request.method == "POST":
        if not flask.request.form["milliseconds"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                milliseconds = int(flask.request.form["milliseconds"])
            except ValueError:
                message = "milliseconds could not be converted to integer"
                success = False
            else:
                response = requests.post(endpoint, timeout=2, json={"milliseconds": milliseconds})
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_delay.html",
        current_page="packet_delay",
        method=flask.request.method,
        success=success,
        message=message,
        milliseconds=response.json()["milliseconds"],
        examples=examples,
    )


@app.route("/packet_loss", methods=["GET", "POST"])
def packet_loss():
    endpoint = _api_url("/disciplines/packet_loss")
    clear_endpoint = _api_url("/disciplines/packet_loss/clear")
    success = True
    message = None
    percent = None
    examples = loss_examples

    if flask.request.method == "POST":
        if not flask.request.form["percent"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                percent = float(flask.request.form["percent"])
            except ValueError:
                message = "percent could not be converted to float"
                success = False
            else:
                response = requests.post(endpoint, timeout=2, json={"percent": percent})
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_loss.html",
        current_page="packet_loss",
        method=flask.request.method,
        success=success,
        message=message,
        percent=response.json()["percent"],
        examples=examples,
    )


@app.route("/packet_duplication", methods=["GET", "POST"])
def packet_duplication():
    endpoint = _api_url("/disciplines/packet_duplication")
    clear_endpoint = _api_url("/disciplines/packet_duplication/clear")
    success = True
    message = None
    percent = None
    examples = duplication_examples

    if flask.request.method == "POST":
        if not flask.request.form["percent"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                percent = float(flask.request.form["percent"])
            except ValueError:
                message = "percent could not be converted to float"
                success = False
            else:
                response = requests.post(endpoint, timeout=2, json={"percent": percent})
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_duplication.html",
        current_page="packet_duplication",
        method=flask.request.method,
        success=success,
        message=message,
        percent=response.json()["percent"],
        examples=examples,
    )


@app.route("/packet_reordering", methods=["GET", "POST"])
def packet_reordering():
    endpoint = _api_url("/disciplines/packet_reordering")
    clear_endpoint = _api_url("/disciplines/packet_reordering/clear")
    success = True
    message = None
    milliseconds = None
    percent = None
    examples = reordering_examples

    if flask.request.method == "POST":
        if not flask.request.form["percent"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                try:
                    milliseconds = float(flask.request.form["milliseconds"])
                except ValueError:
                    message = "milliseconds could not be converted to float"
                    raise
                try:
                    percent = float(flask.request.form["percent"])
                except ValueError:
                    message = "percent could not be converted to float"
                    raise
            except ValueError:
                success = False
            else:
                response = requests.post(endpoint, timeout=2, json={"milliseconds": milliseconds, "percent": percent})
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_reordering.html",
        current_page="packet_reordering",
        method=flask.request.method,
        success=success,
        message=message,
        milliseconds=response.json()["milliseconds"],
        percent=response.json()["percent"],
        examples=examples,
    )


@app.route("/packet_corruption", methods=["GET", "POST"])
def packet_corruption():
    endpoint = _api_url("/disciplines/packet_corruption")
    clear_endpoint = _api_url("/disciplines/packet_corruption/clear")
    success = True
    message = None
    percent = None
    examples = corruption_examples

    if flask.request.method == "POST":
        if not flask.request.form["percent"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                percent = float(flask.request.form["percent"])
            except ValueError:
                message = "percent could not be converted to float"
                success = False
            else:
                response = requests.post(endpoint, timeout=2, json={"percent": percent})
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_corruption.html",
        current_page="packet_corruption",
        method=flask.request.method,
        success=success,
        message=message,
        percent=response.json()["percent"],
        examples=examples,
    )


@app.route("/packet_rate_control", methods=["GET", "POST"])
def packet_rate():
    endpoint = _api_url("/disciplines/packet_rate_control")
    clear_endpoint = _api_url("/disciplines/packet_rate_control/clear")
    success = True
    message = None
    kbit = None
    latency_milliseconds = None
    burst_bytes = None
    examples = rate_examples

    if flask.request.method == "POST":
        if not flask.request.form["kbit"]:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            try:
                try:
                    kbit = int(flask.request.form["kbit"])
                except ValueError:
                    message = "kbit could not be converted to int"
                    raise
                try:
                    latency_milliseconds = int(flask.request.form["latency_milliseconds"])
                except ValueError:
                    message = "milliseconds could not be converted to int"
                    raise
                try:
                    burst_bytes = int(flask.request.form["burst_bytes"])
                except ValueError:
                    message = "bytes could not be converted to int"
                    raise
            except ValueError:
                success = False
            else:
                response = requests.post(
                    endpoint,
                    timeout=2,
                    json={"kbit": kbit, "latency_milliseconds": latency_milliseconds, "burst_bytes": burst_bytes},
                )
                success = response.ok
                message = response.json()["message"]

    response = requests.get(endpoint, timeout=2)
    return _render_template(
        "packet_rate_control.html",
        current_page="packet_rate_control",
        method=flask.request.method,
        success=success,
        message=message,
        kbit=response.json()["kbit"],
        latency_milliseconds=response.json()["latency_milliseconds"],
        burst_bytes=response.json()["burst_bytes"],
        examples=examples,
    )


@app.route("/network_capture", methods=["GET"])
def network_capture():
    return _render_template("network_capture.html", current_page="network_capture", host_url=flask.request.host_url)


@app.route("/network_disconnect", methods=["GET", "POST"])
def network_disconnect():
    endpoint = _api_url("/disconnect")
    success = True
    message = None

    if flask.request.method == "POST":
        network_disconnect = requests.get(endpoint, timeout=2).json()["disconnect"]
        response = requests.post(endpoint, timeout=2, json={"disconnect": not network_disconnect})
        success = response.ok
        message = response.json()["message"]

    network_disconnect = requests.get(endpoint, timeout=2).json()["disconnect"]
    return _render_template(
        "network_disconnect.html",
        current_page="network_disconnect",
        method=flask.request.method,
        success=success,
        message=message,
        network_disconnect=network_disconnect,
    )


@app.route("/network_whitelist", methods=["GET", "POST"])
def network_whitelist():
    endpoint = _api_url("/whitelist")
    clear_endpoint = _api_url("/whitelist/clear")
    success = True
    message = None

    if flask.request.method == "POST":
        whitelist = requests.get(endpoint, timeout=2).json()

        if "remove_from_whitelist" in flask.request.form:
            whitelist.remove({"ip_address": flask.request.form["remove_from_whitelist"]})
        if "add_to_whitelist" in flask.request.form:
            whitelist.append({"ip_address": flask.request.form["add_to_whitelist"]})

        if not whitelist:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            response = requests.post(endpoint, timeout=2, json=whitelist)
            success = response.ok
            message = response.json()["message"]

    whitelist = requests.get(endpoint, timeout=2).json()
    return _render_template(
        "network_whitelist.html",
        current_page="network_whitelist",
        method=flask.request.method,
        success=success,
        message=message,
        whitelist=sorted(map(lambda entry: entry["ip_address"], whitelist)),
    )


@app.route("/network_dnsoverride", methods=["GET", "POST"])
def network_dnsoverride():
    endpoint = _api_url("/dnsoverride")
    clear_endpoint = _api_url("/dnsoverride/clear")
    success = True
    message = None

    if flask.request.method == "POST":
        dns_overrides = requests.get(endpoint, timeout=2).json()

        if "remove_from_dns_override" in flask.request.form:
            dns_overrides.remove(
                {"ip_address": flask.request.form["ip_address"], "hostname": flask.request.form["hostname"]}
            )

        if "add_to_dns_override" in flask.request.form:
            dns_overrides.append(
                {"ip_address": flask.request.form["ip_address"], "hostname": flask.request.form["hostname"]}
            )

        if not dns_overrides:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            response = requests.post(endpoint, timeout=2, json=dns_overrides)
            success = response.ok
            message = response.json()["message"]

    dns_overrides = requests.get(endpoint, timeout=2).json()
    return _render_template(
        "network_dnsoverride.html",
        current_page="network_dnsoverride",
        method=flask.request.method,
        success=success,
        message=message,
        dns_overrides=sorted(dns_overrides, key=lambda k: k["ip_address"]),
    )


@app.route("/network_ip_redirect", methods=["GET", "POST"])
def network_ip_redirect():
    endpoint = _api_url("/ipredirect")
    clear_endpoint = _api_url("/ipredirect/clear")
    success = True
    message = None

    if flask.request.method == "POST":
        ip_redirects = requests.get(endpoint, timeout=2).json()

        if "remove_ip_redirect" in flask.request.form:
            ip_redirects.remove(
                {
                    "ip": flask.request.form["ip"],
                    "port": int(flask.request.form["port"]),
                    "destination_ip": flask.request.form["destination_ip"],
                    "destination_port": int(flask.request.form["destination_port"]),
                    "protocol": flask.request.form["protocol"],
                }
            )

        if "add_ip_redirect" in flask.request.form:
            ip_redirects.append(
                {
                    "ip": flask.request.form["ip"],
                    "port": int(flask.request.form["port"]),
                    "destination_ip": flask.request.form["destination_ip"],
                    "destination_port": int(flask.request.form["destination_port"]),
                    "protocol": flask.request.form["protocol"],
                }
            )

        if not ip_redirects:
            response = requests.post(clear_endpoint)
            success = response.ok
            message = response.json()["message"]
        else:
            response = requests.post(endpoint, timeout=2, json=ip_redirects)
            success = response.ok
            message = response.json()["message"]

    ip_redirects = requests.get(endpoint, timeout=2).json()
    return _render_template(
        "network_ip_redirect.html",
        current_page="network_ip_redirect",
        method=flask.request.method,
        success=success,
        message=message,
        ip_redirects=sorted(ip_redirects, key=lambda k: k["ip"]),
    )


def _render_template(*args, **kwargs):
    kwargs["znail_new_version_available"] = is_update_available()
    kwargs["znail_version"] = __version__
    return flask.render_template(*args, **kwargs)
