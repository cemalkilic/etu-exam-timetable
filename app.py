from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask-marshmallow for serializing/deserializing
from flask_marshmallow import Marshmallow, Schema

import requests
from bs4 import BeautifulSoup

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


# Define an Exam model
class Exam(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String)
    exam_date = db.Column(db.String)
    exam_day = db.Column(db.String)
    exam_time = db.Column(db.String)

    def __init__(self, course_code, course_name, exam_date, exam_day, exam_time):
        self.course_code = course_code
        self.course_name = course_name
        self.exam_date = exam_date
        self.exam_day = exam_day
        self.exam_time = exam_time


class ExamSchema(Schema):

    class Meta:
        # Fields to expose
        fields = ('course_code', 'course_name', 'exam_date', 'exam_day', 'exam_time')


exam_schema = ExamSchema()
exams_schema = ExamSchema(many=True)


def populate_db():
    r = requests.get(app.config['EXAMS_URL'])
    bs = BeautifulSoup(r.content, "lxml")
    table = bs.find('table')
    # to get rid of the first empty row
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    exam_list = list()
    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        tmp = Exam(cols[0], cols[1], cols[6], cols[7], cols[8])
        exam_list.append(tmp)
    return exams_schema.jsonify(exam_list)


@app.route('/')
def hello_world():
    return populate_db() # just to check if we


if __name__ == '__main__':
    app.run()
