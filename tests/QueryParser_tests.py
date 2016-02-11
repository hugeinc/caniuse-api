from nose.tools import *
from features import QueryParser


def test_prep():
    assert_equal(QueryParser.prep('box shadow'), 'box shadow')
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
    qp = QueryParser()
    qp.map.append('ambient-light')
    assert_equal(qp.get_slug(" Ambient Light"), 'ambient-light')