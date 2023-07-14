from flask import Flask, session
from os import path
import os
from datetime import date, timedelta, datetime
  
def break_after_first(value):
  yield value
  raise StopIteration
  
def create_app():
  app = Flask(__name__)
  app.secret_key = os.environ['sessionKey']
  
  from .views import views
  
  app.register_blueprint(views, url_prefix='/')
  
  return app
