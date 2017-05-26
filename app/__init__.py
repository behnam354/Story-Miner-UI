from flask import Flask

# create app
app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object('config')

from app import views
