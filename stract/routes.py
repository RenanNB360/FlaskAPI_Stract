from flask import Blueprint, jsonify
from stract.handlers import get_ads_by_platform, get_summary_by_platform, get_all_ads, get_general_summary

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return jsonify({
        'nome': 'Renan Nunes Bittencourt',
        'email': 'programmerrnb@gmail.com',
        'LinkedIn': 'https://www.linkedin.com/in/renan-nunes-bittencourt-26baa6203/'
    })

@routes.route('/<platform>')
def platform_ads(platform):
    return get_ads_by_platform(platform)

@routes.route('/<platform>/resumo')
def platform_summary(platform):
    return get_summary_by_platform(platform)

@routes.route('/geral')
def all_ads():
    return get_all_ads()

@routes.route('/geral/resumo')
def general_summary():
    return get_general_summary()

def register_routes(app):
    app.register_blueprint(routes)