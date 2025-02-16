# The __init__.py file can contain initialization code that runs when the package is imported.
# It is used to structure and organize submodules or subpackages within a package.

from flask import Flask, jsonify, redirect
import os
from dotenv import load_dotenv
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, Bookmark
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config



load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # tells flask we might have some config outside file

    instance_path = app.instance_path

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    if test_config is None:
        
        app.config.from_mapping(

            SECRET_KEY=os.environ.get("SECRET_KEY", "default_secret_key"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI") or f"sqlite:///{os.path.join(instance_path, 'bookmarks.db')}",
            SQLALCHEMY_TRACK_MODIFICATION = False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'title':"Bookmarks api",
                'uiversion':3
            }
            

        )
    else:
        app.config.from_mapping(test_config)
        
    db.app=app
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    Swagger(app, config=swagger_config, template=template)


    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yml')
    def redirect_to_url(short_url):
        bookmark=Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits +=1
            db.session.commit()

            return redirect(bookmark.url)
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            'error':'Not found'
        }),HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_505(e):
        return jsonify({
            'error':'Something went wrong in the application, please try again'
        }),HTTP_500_INTERNAL_SERVER_ERROR


    return app