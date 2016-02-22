from flask import jsonify, Blueprint

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
    return "The Can I Use API! Needs some HTML!"
