from app_api.views.api_login import api_login



def init_view(app):
    app.register_blueprint(api_login)