import os


def test_cron_hourly_script_to_update_zenterio_ppa_is_present():
    assert os.path.isfile('/etc/cron.hourly/zenterio-ppa-update')


def test_systemd_update_service_is_present():
    assert os.path.isfile('/lib/systemd/system/znail-update.service')
