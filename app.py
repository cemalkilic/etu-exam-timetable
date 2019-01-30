from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask-marshmallow for serializing/deserializing
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()







