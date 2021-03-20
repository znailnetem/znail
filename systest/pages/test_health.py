from ..util import assert_has_title


def test_load_page(znail, health_page):
    assert_has_title(health_page.page, "System Health")
