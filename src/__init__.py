# The __init__.py file can contain initialization code that runs when the package is imported.
# It is used to structure and organize submodules or subpackages within a package.

from flask import Flask, jsonify, redirect
import os
from dotenv import load_dotenv
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from flask_jwt_extended import JWTManager



load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # tells flask we might have some config outside file

    if test_config is None:
        
        app.config.from_mapping(

            SECRET_KEY=os.environ.get("SECRET_KEY", "default_secret_key"),
            SQLALCHEMY_DATABASE_URI= os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATION = False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
            

        )
    else:
        app.config.from_mapping(test_config)
        
    db.app=app
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)


    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits +=1
            db.session.commit()

            return redirect(bookmark.url)



    return app