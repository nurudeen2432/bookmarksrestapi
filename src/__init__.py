# The __init__.py file can contain initialization code that runs when the package is imported.
# It is used to structure and organize submodules or subpackages within a package.

from flask import Flask, jsonify
import os
from dotenv import load_dotenv

from src.auth import auth
from src.bookmarks import bookmarks

from src.database import db



load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # tells flask we might have some config outside file

    if test_config is None:
        
        app.config.from_mapping(

            SECRET_KEY=os.environ.get("SECRET_KEY", "default_secret_key"),
            SQLALCHEMY_DATABASE_URI= os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATION = False
            

        )
    else:
        app.config.from_mapping(test_config)
        
    db.app=app
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)


    return app