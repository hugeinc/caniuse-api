from nose.tools import assert_equal
from caniuse_api.mock import mock_loader
from caniuse_api.apps.caniuse_proxy.service import FeatureService
from caniuse_api.apps.caniuse_proxy.util import QueryParser


def mock_parser():
    # todo seperate this from service
    mock_config = mock_loader.load_mock('features/config')
    features = FeatureService()
    features.parse(mock_config)
    return features.qp


def test_minify():
    qp = QueryParser(['css'])
    assert_equal(qp.minify('svg-css'), 'svgcss')


def test_get_slug():
    qp = mock_parser()
    assert_equal(qp.get_slug("Ambient Light"), 'ambient-light')
    assert_equal(qp.get_slug("Ambient Light"), 'ambient-light')
    assert_equal(qp.get_slug("Trans itions"), 'css-transitions')
    assert_equal(qp.get_slug(' Box shadOw '), 'css-boxshadow')
    assert_equal(qp.get_slug("web-sockets"), 'websockets')
    assert_equal(qp.get_slug("arrowfunctions"), 'arrow-functions')
    assert_equal(qp.get_slug("arrow   functions"), 'arrow-functions')
    assert_equal(qp.get_slug("transforms"), "transforms2d")
    # todo assert_equal(qp.get_slug("transform"), "transforms2d")
    assert_equal(qp.get_slug('svg css'), 'svg-css')
