from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy ()


def init_app ():
  """
  : Create and initialise an Flask App instance for the whole application
  """
  app = Flask (__name__, instance_relative_config=False)
  app.config.from_object ("config.Config")

  # db.init_app (app)

  with app.app_context ():
    # import routes
    from app.home import bp as home_bp
    from app.auth import bp as auth_bp

    # register blueprints
    app.register_blueprint (home_bp)
    app.register_blueprint (auth_bp)

    return app
