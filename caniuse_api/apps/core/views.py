from flask import jsonify, Blueprint, current_app

main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates'
)


@main_blueprint.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@main_blueprint.route('/')
def index():
    #todo more logging
    current_app.logger.info('this works')
    return "The Can I Use API! Needs some HTML!"
