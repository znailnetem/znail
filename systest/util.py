def assert_has_title(page, title):
    for tag in page.find_elements_by_tag_name("h1"):
        if tag.text == title:
            break
    else:
        raise AssertionError('Page did not contain title "{title}"'.format(title=title))


def assert_upgrade_alert_is_shown(page):
    try:
        page.find_element_by_class_name("alert-info")
    except Exception:
        raise AssertionError("Upgrade alert not showing")


def assert_success_alert_is_shown(page):
    try:
        page.find_element_by_class_name("alert-success")
    except Exception:
        raise AssertionError("Success alert not showing")


def assert_danger_alert_is_shown(page):
    try:
        page.find_element_by_class_name("alert-danger")
    except Exception:
        raise AssertionError("Danger alert not showing")
