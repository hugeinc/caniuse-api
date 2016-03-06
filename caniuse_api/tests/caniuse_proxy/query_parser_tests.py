from nose.tools import assert_equal
from caniuse_api.apps.caniuse_proxy.util import QueryParser


def test_minify():
    qp = QueryParser(['css'])
    assert_equal(qp.minify('svg-css'), 'svgcss')


def test_convert_to_slug():
    qp = QueryParser()
    qp.add_valid_slug('ambient-light')
    qp.add_valid_slug('arrow-functions')
    assert_equal(qp.get_slug('Ambient Light'), 'ambient-light')
    assert_equal(qp.get_slug("arrowfunctions"), 'arrow-functions')


def test_prefixes():
    qp = QueryParser(['css'])
    qp.add_valid_slug('css-transitions')
    qp.add_valid_slug('css-boxshadow')
    qp.add_valid_slug('svg-css')
    assert_equal(qp.get_slug('Trans itions'), 'css-transitions')
    assert_equal(qp.get_slug(' Box shadOw '), 'css-boxshadow')
    assert_equal(qp.get_slug('svg css'), 'svg-css')


def test_hyphen_removal():
    qp = QueryParser()
    qp.add_valid_slug('websockets')
    assert_equal(qp.get_slug('web-sockets'), 'websockets')


def test_space_removal():
    qp = QueryParser()
    qp.add_valid_slug('arrow-functions')
    assert_equal(qp.get_slug("arrow   functions"), 'arrow-functions')


def test_suffix_removal():
    qp = QueryParser([], ['2d'])
    qp.add_valid_slug('transforms2d')
    assert_equal(qp.get_slug("transforms"), "transforms2d")
