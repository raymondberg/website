from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import *
import csv
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///costuming.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)

db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Costume(db.Model):
    __tablename__ = 'costume'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(120))
    character_series = db.Column(db.String(120))
    character_variation = db.Column(db.String(120))
    costumer_key = db.Column(db.Integer, unique=False, nullable=False)
    resource_key = db.Column(db.Integer, unique=False, nullable=False)
    month_completed = db.Column(db.Integer, unique=False, nullable=False)
    year_completed = db.Column(db.Integer)
    media_type = db.Column(db.String(120))
    property = db.Column(db.String(120))

class BLM_Links(db.Model):
    __tablename__ = 'blm_links'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120))
    name = db.Column(db.String(120))
    category= db.Column(db.String(120))

class Images(db.Model):
    __tablename__ = 'images'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    costume_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(120))

@app.route('/character_name>/<character_series>/<character_variation>')
def create(character_name, character_series, character_variation):
    costume = Costume(character_name=character_name, character_series=character_series, character_variation=character_variation)
    db.session.add(costume)
    db.session.commit()
    return '<h1>Added new Costume!</h1>'

class CostumeForm(FlaskForm):
    character_name = StringField('Character Name', validators=[DataRequired()])
    character_series = StringField('Character Series', validators=[DataRequired()])
    character_variation = StringField('Variation', validators=[DataRequired()])
    media_type = StringField('Media Type', validators=[DataRequired()])
    completed = BooleanField('Completed?')
    submit = SubmitField('Submit')

@app.route('/action_page')
def form_submit():
    return render_template('action_page.html')

@app.route('/costumes-<id>')
def get_costume(id):
    costume = Costume.query.filter_by(id=id).first()
    images = Images.query.all()
    title = str(costume.character_name)
    costume_images = []
    for image in images:
        if image.costume_id == costume.id:
            costume_images.append(image.image_url)
        else:
            pass
    return render_template('costume.html', title=title, costume=costume, costume_images=costume_images)

def create(character_name, character_series, character_variation):
    costume = Costume(character_name=character_name, character_series=character_series, character_variation=character_variation)
    db.session.add(costume)
    db.session.commit()
    return character_name

@app.route('/all', methods=['GET', 'POST'])
def get_all():
    total = Costume.query.count()
    all_costumes = Costume.query.all()
    form = CostumeForm()
    if form.validate_on_submit():
        print("The CHARACTER IS:", form.character_name)

        ### FLASH ISN'T WORKING
        flash('Costume Submission for {}'.format(
            form.character_name.data, form.character_series.data, form.character_variation.data, form.media_type.data))
        return redirect('/all') #add a failed page?
    return render_template('all_costumes.html', title='All Costumes',  costumes=all_costumes, total=total, form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blm')
def blm():
    links = BLM_Links.query.all()
    link_cat = []
    for link in links:
        if link.category not in link_cat:
            link_cat.append(link.category)
        else:
            pass
    return render_template('blm.html', title='Black Lives Matter', links=links, link_cat=link_cat)

@app.route('/about')
def about():
    return render_template('about.html', title='About Me')

if __name__ == '__main__':
    app.run(debug=True)
