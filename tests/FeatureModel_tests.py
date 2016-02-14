from nose.tools import *
from features import FeatureModel
from mock import mock_loader


def test_stat_parse():
    mock = mock_loader.load_mock('features/transforms2d')
    feature = FeatureModel("transforms2d")
    feature.parse({"stats":mock.get('stats')})
    assert_equals(feature.support.get('safari').get('y'), '9')
    assert_equals(feature.support.get('opera').get('n'), '9')


def test_float_versions():
    assert_equals(FeatureModel.float_version('9.1'), 9.1)


def test_float_multiple_versions():
    assert_equals(FeatureModel.float_multiple_versions('9.1'), 9.1)
    assert_equals(FeatureModel.float_multiple_versions('9.1-9.3'), 9.1)
    assert_equals(FeatureModel.float_multiple_versions('4.4.3-4.4.4'), 4.43)


def test_float_sem_ver():
    assert_equals(FeatureModel.float_sem_ver('9'), 9)
    assert_equals(FeatureModel.float_sem_ver('6.7.8.9'), 6.789)
    assert_true(FeatureModel.float_sem_ver('6.7.8') > FeatureModel.float_sem_ver('6.7'))
