import collections
from flask import render_template
from caniuse_api.apps.hipchat import HipChatMessage, HipChatResponse

browser_map = collections.OrderedDict()
browser_map['ie'] = 'IE'
browser_map['ios_saf'] = 'iOS'
browser_map['android'] = 'Android'
browser_map['firefox'] = 'Firefox'
browser_map['chrome'] = 'Chrome'
browser_map['safari'] = 'Safari'
browser_map['edge'] = 'Edge'
browser_map['opera'] = 'Opera'


class CanIUseBot(object):

    def __init__(self, feature_service):
        self.features = feature_service

    def parse_request(self, request_json):
        message = HipChatMessage(request_json)
        if message.content:
            feature = self.features.search(message.content)
            if feature and feature.data:
                response = HipChatResponse(
                    render_template(
                        'hipchat/feature_support_message.html',
                        feature=feature, browser_map=browser_map
                    )
                )
            else:
                # todo have a list all available features command
                response = HipChatResponse("Feature not found", 'red')
        else:
            # todo output a template that lists instructions
            response = HipChatResponse("No message content. Reply with a help command.", 'gray')
        return response