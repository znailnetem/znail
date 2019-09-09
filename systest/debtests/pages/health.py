from zaf.component.decorator import component, requires

from ..util import assert_has_title


@component
@requires(page_loader="PageLoader", args=['http://localhost/health'])
class HealthPage(object):

    def __init__(self, page_loader):
        self._page_loader = page_loader

    @property
    def page(self):
        return self._page_loader.page


@requires(znail="Znail")
@requires(health_page="HealthPage")
def test_load_page(znail, health_page):
    assert_has_title(health_page.page, 'System Health')
