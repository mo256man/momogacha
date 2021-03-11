from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///momo.db"
# app.config["SECRET_KEY"] = '\xf4\x1b.\x04\xba\xfc-c\x1cg\x8eV\xe9\xa6w}\xa7\xfc*zQnq\xed'
db = SQLAlchemy(app)

import application.views  # noqa: F401
