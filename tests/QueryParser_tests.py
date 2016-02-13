from nose.tools import *
from features import QueryParser


def test_prep():
    assert_equal(QueryParser.prep('box shadow'), 'box shadow')
    assert_equal(QueryParser.prep('box  shadow '), 'box shadow')
    assert_equal(QueryParser.prep(' Box shadOw '), 'box shadow')
    assert_equal(QueryParser.prep('Box+shadoW '), 'box shadow')


def test_slugify():
    assert_equal(QueryParser.slugify('box shadow'), 'box-shadow')
    assert_equal(QueryParser.slugify('background position x y'), 'background-position-x-y')


def test_condense():
    assert_equal(QueryParser.condense('blob builder'), 'blobbuilder')


def test_prepend():
    assert_equal(QueryParser.prepend('box-shadow', 'css'), 'css-box-shadow')
    assert_equal(QueryParser.prepend('tabsize', 'css3'), 'css3-tabsize')


def test_get_slug():
    # todo more tests!
    qp = QueryParser(['css', 'css3'])
    qp.add_valid_slug('web-sockets')
    qp.add_valid_slug('ambient-light')
    qp.add_valid_slug('css-transitions')
    qp.add_valid_slug('arrow-functions')
    qp.add_valid_slug('websockets')
    assert_equal(qp.get_slug("Ambient Light"), 'ambient-light')
    assert_equal(qp.get_slug("Ambient Light"), 'ambient-light')
    assert_equal(qp.get_slug("Transitions"), 'css-transitions')
    #todo fix these
    assert_equal(qp.get_slug("web-sockets"), 'websockets')
    assert_equal(qp.get_slug("arrowfunctions"), 'arrow-functions')
