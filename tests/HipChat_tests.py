from nose.tools import *
from hipchat import HipChatMessage


def get_msg_mock(msg, name="Your Name", mentions=None, mention_name="Blinky"):

    formatted_mentions = []
    for name in mentions or []:
        formatted_mentions.append({'mention_name': name})
    msg = {
        "mentions": formatted_mentions,
        "from": {
            "mention_name": mention_name,
            "name": name
        },
        "message": msg
    }
    return {
        "item": {
            "message": msg
        }
    }


def test_separate_slug():
    msg = "/mycmd CSS Transitions"
    assert_equals(HipChatMessage.separate_command(msg), ('/mycmd', 'CSS Transitions'))


def test_seperate_slug_inverted():
    msg = "CSS Transitions /mycmd"
    assert_equals(HipChatMessage.separate_command(msg), ('/mycmd', 'CSS Transitions'))


def test_seperate_slug_only():
    msg = "/mycmd"
    assert_equals(HipChatMessage.separate_command(msg), ('/mycmd', ''))


def test_seperate_mention():
    msg = "@Geddy CSS Transitions"
    assert_equals(HipChatMessage.separate_mentions(msg, ['Geddy']), 'CSS Transitions')


def test_seperate_mentions():
    msg = "@Geddy CSS @Alex Transitions"
    assert_equals(HipChatMessage.separate_mentions(msg, ['Geddy', 'Alex']), 'CSS Transitions')


def test_get_msg():
    msg = HipChatMessage(get_msg_mock("/mycmd CSS Transitions"))
    assert_equals((msg.content, msg.cmd_slug), ('CSS Transitions', '/mycmd'))


def test_mentions():
    msg = HipChatMessage(get_msg_mock("/mycmd @Oates CSS Transitions", "Hall", ["Oates"]))
    assert_equals(msg.mentions, ['Oates'])


def test_msg_w_mentions():
    msg = HipChatMessage(get_msg_mock("/mycmd @Oates CSS Transitions", "Hall", ["Oates"]))
    assert_equals((msg.content, msg.cmd_slug), ('CSS Transitions', '/mycmd'))


def test_get_msg_just_slug():
    msg = HipChatMessage(get_msg_mock("/mycmd"))
    assert_equals((msg.content, msg.cmd_slug), (None, '/mycmd'))


def test_slug_after_body():
    msg = HipChatMessage(get_msg_mock("Arrow Functions /mycmd"))
    assert_equals((msg.content, msg.cmd_slug), ("Arrow Functions", '/mycmd'))


def test_slug_after_body_w_mentions():
    msg = HipChatMessage(get_msg_mock("arrow functions /mycmd @Yoda", "JarJar", ["Yoda"]))
    assert_equals((msg.content, msg.cmd_slug), ("arrow functions", '/mycmd'))


def test_get_msg_none():
    msg = HipChatMessage({})
    assert_equals((msg.content, msg.cmd_slug), (None, None))
