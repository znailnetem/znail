from zaf.component.decorator import component, requires

from ..util import assert_has_title


@component
@requires(page_loader="PageLoader", args=['http://localhost/about'])
class AboutPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page


@requires(znail="Znail")
@requires(about_page="AboutPage")
def test_load_page(znail, about_page):
    assert_has_title(about_page.page, 'About')
