from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os
import logging

# Initializes app
app = Flask(__name__)
homedir = os.path.abspath(os.path.dirname(__file__))

# Database location + secret key for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(homedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2496c6d62b0c524876c5e05ce420677651e7e38bd0383609'

# Initializes DB
db = SQLAlchemy(app)

# Initializes Marshmallow
ma = Marshmallow(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, email, campus):
        self.name = name
        self.email = email
        self.campus = campus

# Creates DB
db.create_all()

# Form Schema
class FormSchema(ma.Schema):
    class Meta:
       fields = ('id', 'name', 'email', 'campus')

# Initialize Schema
form_schema = FormSchema()
forms_schema = FormSchema(many=True)

# Display index
@app.route('/')
def index():
    return render_template('index.html')

# Obtain form data
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        campus = request.form['campus']

        if not name:
            flash('Name is required')
        elif not email:
            flash('Email is required')
        elif not city:
            flash('Campus is required')
        else:
            new_reg = Form(name, email, campus)
            db.session.add(new_reg)
            try:
                db.session.commit()
                # Logging user creation event
                logging.basicConfig(filename='creation.log', encoding='utf-8', level=logging.NOTSET)
                logging.info('{} - {} \n'.format(name, datetime.now()))
            except Exception as e:
                # logging
                flash('Name or Email already on record')
            return render_template('create.html')

    return render_template('create.html')

# Get all regs
@app.route('/all/', methods=['GET'])
def all():
    all_regs = Form.query.all()
    results = forms_schema.dump(all_regs)
    return render_template('all.html', results=results)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
