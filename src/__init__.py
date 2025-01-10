# The __init__.py file can contain initialization code that runs when the package is imported.
# It is used to structure and organize submodules or subpackages within a package.

from flask import Flask, jsonify
import os

from src.auth import auth
from src.bookmarks import bookmarks




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # tells flask we might have some config outside file

    if test_config is None:
        
        app.config.from_mapping(

            SECRET_KEY=os.environ.get("SECRET_KEY", "default_secret_key")
            

        )
    else:
        app.config.from_mapping(test_config)
        

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)


    return app