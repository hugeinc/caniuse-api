from nose.tools import assert_equals
from caniuse_api.apps.caniuse_proxy.model import FeatureModel
from caniuse_api.apps.caniuse_bot import browser_map
from caniuse_api.mock import mock_loader


def get_feature_model(slug):
    mock = mock_loader.load_mock('features/%s' % slug)
    feature = FeatureModel(slug)
    feature.parse(mock)
    return feature


def test_stat_parse():
    feature = get_feature_model('transforms2d')
    assert_equals(feature.support.get('safari').get('y'), '9')
    assert_equals(feature.support.get('opera').get('n'), '9')


def test_get_min_support_by_flags():
    feature = get_feature_model('flexbox')
    flags = ['y x', 'a', 'a x']

    version, notes = feature.get_min_support_by_flags('opera', flags)
    assert_equals(version, '15')
    assert_equals(len(notes), 0)

    version, notes = feature.get_min_support_by_flags('ie', flags)
    assert_equals(version, '11')
    assert_equals(len(notes), 1)


def test_get_version_notes_from_flag():
    feature = get_feature_model('flexbox')
    flag, notes = feature.get_version_notes_from_flag('a x #4 #3')
    assert_equals(flag, 'a x')
    assert_equals(len(notes), 2)
    flag, notes = feature.get_version_notes_from_flag('a #4')
    assert_equals(flag, 'a')
    assert_equals(len(notes), 1)
    flag, notes = feature.get_version_notes_from_flag('y x')
    assert_equals(flag, 'y x')
    assert_equals(notes, None)


def test_get_version_notes_from_supported_flag():
    feature = get_feature_model('svg')
    flag, notes = feature.get_version_notes_from_flag('y #2')
    assert_equals(flag, 'y')
    assert_equals(len(notes), 1)


def test_get_relevant_notes():
    feature = get_feature_model('websockets')
    flags = ['y x', 'a', 'a x']
    keys = browser_map.keys()
    notes = feature.get_relevant_notes(keys, flags)
    assert_equals(len(notes), 3)


def test_get_relevant_notes_supported():
    feature = get_feature_model('svg')
    browser_ids = browser_map.keys()
    flags = ['y'], ['y x', 'a', 'a x']
    notes = feature.get_relevant_notes(browser_ids, flags)
    assert_equals(len(notes), 2)
