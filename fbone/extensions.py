# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.login import LoginManager


db = SQLAlchemy()
mail = Mail()
cache = Cache()
login_manager = LoginManager()
