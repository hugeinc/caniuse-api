from nose.tools import assert_equals, assert_greater
from caniuse_api.apps.caniuse_proxy.util import float_sem_ver
from caniuse_api.apps.caniuse_proxy.util import float_version
from caniuse_api.apps.caniuse_proxy.util import float_multiple_versions


def test_float_versions():
    assert_equals(float_version('9.1'), 9.1)


def test_float_multiple_versions():
    assert_equals(float_multiple_versions('9.1'), 9.1)
    assert_equals(float_multiple_versions('9.1-9.3'), 9.1)
    assert_equals(float_multiple_versions('4.4.3-4.4.4'), 4.43)


def test_float_sem_ver():
    assert_equals(float_sem_ver('9'), 9)
    assert_equals(float_sem_ver('6.7.8.9'), 6.789)
    assert_greater(float_sem_ver('6.7.8'), float_sem_ver('6.7'))
