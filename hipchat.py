
class HipChatMessage(object):

    @staticmethod
    def separate_mentions(msg, mentions):
        for name in mentions:
            handle = ''.join(['@', name])  # todo if HipChat doesnt append "@", remove this line
            if handle in msg:
                parts = msg.split()
                parts.remove(handle)
                msg = ' '.join(parts)
        return msg

    @staticmethod
    def separate_command(msg):
        slug_index = msg.index('/')
        parts = msg.split(' ')
        for i in range(len(parts)):
            if msg.index(parts[i]) == slug_index:
                cmd_slug = parts[i:i+1][0].strip()
                parts.remove(cmd_slug)
                return cmd_slug, ' '.join(parts).strip()

    mentions = []
    content = None
    cmd_slug = None

    def __init__(self, json_data):
        self.parse(json_data.get('item', {}).get('message'))

    def parse(self, data):
        try:
            for user in data.get('mentions', []):
                self.mentions.append(user.get('mention_name'))
            self.cmd_slug, body = HipChatMessage.separate_command(data.get('message', ''))
            content = HipChatMessage.separate_mentions(body, self.mentions)
            self.content = content if len(content) else None
            return True
        except (AttributeError, ValueError, TypeError):
            return False


class HipChatResponse(object):

    def __init__(self, message, color="green", notify=False, message_format="html"):
        self.data = {
            "color": color,
            "message": message,
            "notify": notify,
            "message_format": message_format
        }


class ICanHazBot(object):

    def __init__(self, feature_service):
        self.features = feature_service

    def parse_request(self, request_json):
        message = HipChatMessage(request_json)
        if message.content:
            feature = self.features.search(message.content)
            if feature:
                # todo handle exceptions
                feature.load()
                response = HipChatResponse(feature.data.get('description'))
            else:
                response = HipChatResponse("Feature not found", 'red')
        else:
            response = HipChatResponse("No message content. Reply with a help command.", 'gray')
        return response
