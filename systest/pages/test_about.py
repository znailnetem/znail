from ..util import assert_has_title


def test_load_page(znail, about_page):
    assert_has_title(about_page.page, "About")
