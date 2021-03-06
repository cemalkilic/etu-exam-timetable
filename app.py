from flask import Flask, make_response

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask-marshmallow for serializing/deserializing
from flask_marshmallow import Marshmallow, Schema

# Import heroku
from flask_heroku import Heroku

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)


# Define an Exam model
class Exam(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, nullable=False)
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


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


def populate_db():
    r = requests.get(app.config['EXAMS_URL'])
    bs = BeautifulSoup(r.content, "lxml")
    table = bs.find('table')
    # to get rid of the first empty row
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    exam_list = list()
    existing_exam = list()

    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]

        # a quicky check
        # it does not hurt to create
        # a dict for this purpose
        exam = {
            "course_code"   : cols[0],
            "exam_date"     : cols[6]
        }
        if exam in existing_exam:
            continue

        # if course_code not exist append it
        # and create an exam object for it
        existing_exam.append(exam)
        exam_obj = Exam(cols[0], cols[1], cols[6], cols[7], cols[8])
        exam_list.append(exam_obj)

        # if there is any mutual courses (you should view the exam table)
        # create a new exam for that one
        mutual_course_code = cols[2]
        if mutual_course_code != '':
            another_exam = Exam(mutual_course_code, cols[1], cols[6], cols[7], cols[8])
            exam_list.append(another_exam)
            existing_exam.append(mutual_course_code)

    # this insertion should be done in
    # more beautiful way
    # but it's enough for now :(

    # insert all exams to db
    # after checking it exists
    for exam in exam_list:
        exists = Exam.query.filter(Exam.course_code == exam.course_code)\
            .filter(Exam.exam_date == exam.exam_date).first()
        if not exists:
            db.session.add(exam)
    db.session.commit()
    return exams_schema.jsonify(exam_list)


@app.route('/')
def hello_world():
    return populate_db() # just to check if we


@app.route('/exam/<course_code>')
def course_exams(course_code):
    # I assumed that no problem with turkish characters
 	# so BIL-361 input is welcomed however bil-361 is not
    # firstly, we need to check if course_code has the right syntax
    content = course_code.split(' ')
    #
    if len(content) != 2:
        return "Course code must be like: ABC 123"

    if len(content[0]) != 3 or len(content[1]) != 3:
        return "Course code must be like: ABC 123"

    if not content[0].isupper():
        return "Course code first part must be upper case letters: ABC 123"

    if not content[1].isdigit():
        return "Course code second part must be digits: ABC 123"

    # if we are here, course_code is okay to query
    result = Exam.query.filter(Exam.course_code == course_code)

    response = exams_schema.jsonify(result)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
