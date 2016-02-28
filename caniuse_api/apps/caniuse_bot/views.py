from flask import request, jsonify, Blueprint
from caniuse_api.apps.caniuse_proxy.service import FeatureService
from caniuse_api.apps.caniuse_bot import CanIUseBot
from caniuse_api.apps.core.auth import authorized

bot_blueprint = Blueprint(
    'caniuse_bot',
    __name__,
    template_folder='templates'
)


@bot_blueprint.route('/hipchat', methods=['POST'])
@authorized
def hip_chat():
    features = FeatureService.get_instance()
    bot = CanIUseBot(features)
    response = bot.parse_request(request.get_json())
    return jsonify(response.data)
