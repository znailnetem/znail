from builtins import ConnectionRefusedError
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .util import assert_danger_alert_is_shown, assert_success_alert_is_shown
import logging
import pytest
import socket
import subprocess
import time

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.DEBUG)


class _Znail:
    def __init__(
        self,
        env=None,
        override_iptables="echo",
        override_tc="echo",
        override_hub_ctrl="echo",
        override_service="echo",
        override_systemctl="echo",
        override_hosts_file="/dev/null",
        override_dnsmasq_overrides_file="/dev/null",
    ):

        znail_entry_point = subprocess.check_output(["which", "znail"], universal_newlines=True).strip()

        self.env = env
        self.znail_command = (
            "export IPTABLES_COMMAND={override_iptables} && "
            "export TC_COMMAND={override_tc} && "
            "export HUB_CTRL_COMMAND={hub_ctrl_command} && "
            "export SERVICE_COMMAND={override_service} && "
            "export SYSTEMCTL_COMMAND={override_systemctl} && "
            "export ZNAIL_FORCE_INTERFACE_UP=1 && "
            "export HOSTS_FILE={override_hosts_file} && "
            "export DNSMASK_OVERRIDES_FILE={override_dnsmasq_overrides_file} && "
            "{entry_point} --port 8080"
        ).format(
            entry_point=znail_entry_point,
            override_iptables=override_iptables,
            hub_ctrl_command=override_hub_ctrl,
            override_tc=override_tc,
            override_service=override_service,
            override_systemctl=override_systemctl,
            override_hosts_file=override_hosts_file,
            override_dnsmasq_overrides_file=override_dnsmasq_overrides_file,
        )

    def _start_znail_process(self):
        logger.debug("Running znail command: {command}".format(command=self.znail_command))
        env = self.env.copy() if self.env else {}
        env.update({"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"})
        self.process = subprocess.Popen(
            self.znail_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            universal_newlines=True,
        )

    def _wait_for_znail_process_to_become_ready(self, timeout=5):
        logger.debug("Waiting for Znail to start")
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            try:
                s = socket.socket(socket.AF_INET)
                s.connect(("localhost", 8080))
            except ConnectionRefusedError:
                pass
            else:
                logger.debug("Znail is listening on port 8080")
                s.close()
                break

    def __enter__(self):
        self._start_znail_process()
        self._wait_for_znail_process_to_become_ready()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        kill_process = subprocess.Popen("killall -2 znail", stdout=subprocess.PIPE, shell=True)
        kill_process.wait()

        self.stdout, self.stderr = self.process.communicate()
        logger.debug("-------- stdout --------")
        for line in self.stdout.split("\n"):
            logger.debug(line)
        logger.debug("-------- end stdout --------")
        logger.debug("-------- stderr --------")
        for line in self.stderr.split("\n"):
            logger.debug(line)
        logger.debug("-------- end stderr --------")


class _PageLoader:
    def __init__(self, url):
        options = Options()
        options.add_argument("-headless")

        self._url = url
        self._driver = webdriver.Firefox(options=options)

    @property
    def page(self):
        try:
            self._driver.get(self._url)
        except Exception:
            raise AssertionError('Could not load page "{url}"'.format(url=self._url))
        return self._driver

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        try:
            self._driver.close()
        except Exception:
            pass


class _AboutPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page


class _HealthPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page


class _DisconnectPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def toggle(self):
        page = self.page
        page.find_element_by_id("submit").click()
        assert_success_alert_is_shown(page)


class _DnsOverridePage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip_address, hostname, expect_success=True):
        page = self.page
        ip_address_input = page.find_element_by_name("ip_address")
        hostname_input = page.find_element_by_name("hostname")
        ip_address_input.clear()
        hostname_input.clear()
        if ip_address:
            ip_address_input.send_keys(ip_address)
        hostname_input.send_keys(hostname)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip_address, hostname):
        page = self.page
        page.find_element_by_id(
            "remove_{ip_address}_{hostname}".format(ip_address=ip_address if ip_address else "", hostname=hostname)
        ).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        dnsoverride = []
        rows = page.find_elements_by_tag_name("tr")
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name("td")
            dnsoverride.append((columns[0].text, columns[1].text))
        return dnsoverride


class _IpRedirectPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip, port, destination_ip, destination_port, protocol, expect_success=True):
        page = self.page
        ip_input = page.find_element_by_name("ip")
        port_input = page.find_element_by_name("port")
        destination_ip_input = page.find_element_by_name("destination_ip")
        destination_port_input = page.find_element_by_name("destination_port")
        protocol_input = page.find_element_by_name("protocol")
        ip_input.clear()
        port_input.clear()
        destination_ip_input.clear()
        destination_port_input.clear()
        ip_input.send_keys(ip)
        port_input.send_keys(port)
        destination_ip_input.send_keys(destination_ip)
        destination_port_input.send_keys(destination_port)
        for option in protocol_input.find_elements_by_tag_name("option"):
            if option.text == protocol:
                option.click()
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip, port, destination_ip, destination_port, protocol):
        page = self.page
        page.find_element_by_id(
            "remove_{ip}_{port}_{destination_ip}_{destination_port}_{protocol}".format(
                ip=ip, port=port, destination_ip=destination_ip, destination_port=destination_port, protocol=protocol
            )
        ).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        ip_redirect = []
        rows = page.find_elements_by_tag_name("tr")
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name("td")
            ip_redirect.append(
                (columns[0].text, int(columns[1].text), columns[2].text, int(columns[3].text), columns[4].text)
            )
        return ip_redirect


class _WhitelistPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def add(self, ip_address, expect_success=True):
        page = self.page
        add_to_whitelist_input = page.find_element_by_name("add_to_whitelist")
        add_to_whitelist_input.clear()
        add_to_whitelist_input.send_keys(ip_address)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)

    def remove(self, ip_address):
        page = self.page
        page.find_element_by_id("remove_{ip_address}".format(ip_address=ip_address)).click()
        assert_success_alert_is_shown(page)

    def get(self):
        page = self.page
        whitelist = []
        rows = page.find_elements_by_tag_name("tr")
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name("td")
            whitelist.append(columns[0].text)
        return whitelist


class _PacketCorruptionPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        try:
            return float(percent_input.get_attribute("value"))
        except ValueError:
            return None

    def set(self, percent=None, expect_success=True):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        percent_input.clear()
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _PacketDelayPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        milliseconds_input = page.find_element_by_name("milliseconds")
        try:
            return int(milliseconds_input.get_attribute("value"))
        except ValueError:
            return None

    def set(self, milliseconds=None, expect_success=True):
        page = self.page
        milliseconds_input = page.find_element_by_name("milliseconds")
        milliseconds_input.clear()
        if milliseconds:
            milliseconds_input.send_keys(milliseconds)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _PacketDuplicationPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        try:
            return float(percent_input.get_attribute("value"))
        except ValueError:
            return None

    def set(self, percent=None, expect_success=True):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        percent_input.clear()
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _PacketLossPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        try:
            return float(percent_input.get_attribute("value"))
        except ValueError:
            return None

    def set(self, percent=None, expect_success=True):
        page = self.page
        percent_input = page.find_element_by_name("percent")
        percent_input.clear()
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _PacketRateControlPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        kbit_input = page.find_element_by_name("kbit")
        latency_milliseconds_input = page.find_element_by_name("latency_milliseconds")
        burst_bytes_input = page.find_element_by_name("burst_bytes")
        try:
            return (
                int(kbit_input.get_attribute("value")),
                int(latency_milliseconds_input.get_attribute("value")),
                int(burst_bytes_input.get_attribute("value")),
            )
        except ValueError:
            return None

    def set(self, kbit=None, latency_milliseconds=None, burst_bytes=None, expect_success=True):
        page = self.page
        kbit_input = page.find_element_by_name("kbit")
        latency_milliseconds_input = page.find_element_by_name("latency_milliseconds")
        burst_bytes_input = page.find_element_by_name("burst_bytes")
        kbit_input.clear()
        latency_milliseconds_input.clear()
        burst_bytes_input.clear()
        if kbit:
            kbit_input.send_keys(kbit)
        if latency_milliseconds:
            latency_milliseconds_input.send_keys(latency_milliseconds)
        if burst_bytes:
            burst_bytes_input.send_keys(burst_bytes)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _PacketReorderingPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    def get(self):
        page = self.page
        milliseconds_input = page.find_element_by_name("milliseconds")
        percent_input = page.find_element_by_name("percent")
        try:
            return (
                int(milliseconds_input.get_attribute("value")),
                float(percent_input.get_attribute("value")),
            )
        except ValueError:
            return None

    def set(self, milliseconds=None, percent=None, expect_success=True):
        page = self.page
        milliseconds_input = page.find_element_by_name("milliseconds")
        percent_input = page.find_element_by_name("percent")
        milliseconds_input.clear()
        percent_input.clear()
        if milliseconds:
            milliseconds_input.send_keys(milliseconds)
        if percent:
            percent_input.send_keys(percent)
        page.find_element_by_id("submit").click()
        if expect_success:
            assert_success_alert_is_shown(page)
        else:
            assert_danger_alert_is_shown(page)


class _IndexPage:
    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page

    @property
    def overview(self):
        page = self.page
        result = {}
        rows = page.find_elements_by_tag_name("tr")
        for row in rows[1:]:
            columns = row.find_elements_by_tag_name("td")
            name = columns[0].text
            status = columns[1].text == "Active"
            result[name] = status
        return result


@pytest.fixture
def Znail():
    return _Znail


@pytest.fixture
def znail():
    with _Znail() as _znail:
        yield _znail


@pytest.fixture
def PageLoader():
    return _PageLoader


@pytest.fixture
def about_page(PageLoader):
    with PageLoader("http://localhost:8080/about") as page_loader:
        yield _AboutPage(page_loader)


@pytest.fixture
def health_page(PageLoader):
    with PageLoader("http://localhost:8080/health") as page_loader:
        yield _HealthPage(page_loader)


@pytest.fixture
def disconnect_page(PageLoader):
    with PageLoader("http://localhost:8080/network_disconnect") as page_loader:
        yield _DisconnectPage(page_loader)


@pytest.fixture
def dns_override_page(PageLoader):
    with PageLoader("http://localhost:8080/network_dnsoverride") as page_loader:
        yield _DnsOverridePage(page_loader)


@pytest.fixture
def ip_redirect_page(PageLoader):
    with PageLoader("http://localhost:8080/network_ip_redirect") as page_loader:
        yield _IpRedirectPage(page_loader)


@pytest.fixture
def whitelist_page(PageLoader):
    with PageLoader("http://localhost:8080/network_whitelist") as page_loader:
        yield _WhitelistPage(page_loader)


@pytest.fixture
def packet_corruption_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_corruption") as page_loader:
        yield _PacketCorruptionPage(page_loader)


@pytest.fixture
def packet_delay_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_delay") as page_loader:
        yield _PacketDelayPage(page_loader)


@pytest.fixture
def packet_duplication_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_duplication") as page_loader:
        yield _PacketDuplicationPage(page_loader)


@pytest.fixture
def packet_loss_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_loss") as page_loader:
        yield _PacketLossPage(page_loader)


@pytest.fixture
def packet_rate_control_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_rate_control") as page_loader:
        yield _PacketRateControlPage(page_loader)


@pytest.fixture
def packet_reordering_page(PageLoader):
    with PageLoader("http://localhost:8080/packet_reordering") as page_loader:
        yield _PacketReorderingPage(page_loader)


@pytest.fixture
def index_page(PageLoader):
    with PageLoader("http://localhost:8080/") as page_loader:
        yield _IndexPage(page_loader)
