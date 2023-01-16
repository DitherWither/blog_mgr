import os
from os import environ
import dotenv

import requests

from flask import Flask
from flaskext.markdown import Markdown

import blog_mgr.auth
import blog_mgr.blog
import blog_mgr.db
from blog_mgr.blog import bp


dotenv.load_dotenv(dotenv.find_dotenv())
# Create and configure app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=environ.get('SECRET_KEY'),
)

Markdown(app)
blog_mgr.db.init_app(app)

static_path = os.path.dirname(__file__) + '/static'
main_css_path = static_path + '/assets/main.css'

if not os.path.isfile(main_css_path):
    os.system(f"cd {static_path} && npm install && npm run build")

app.register_blueprint(blog_mgr.auth.bp)

app.add_url_rule('/', endpoint='blog.index')
app.register_blueprint(bp)
