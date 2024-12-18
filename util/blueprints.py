import routes


def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.coaches)
    app.register_blueprint(routes.games)
    app.register_blueprint(routes.players)
    app.register_blueprint(routes.teams)
    app.register_blueprint(routes.user)
