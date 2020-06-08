from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import render_template
import csv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///costuming.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/costumes/<id>')
def get_costume(id):
    costume = Costume.query.filter_by(id=id).first()
    images = Images.query.all()
    costume_images = []
    for image in images:
        if image.costume_id == costume.id:
            costume_images.append(image.image_url)
        else:
            pass
    return render_template('costume.html', costume=costume, costume_images=costume_images)

@app.route('/all')
def get_all():
    total = Costume.query.count()
    all_costumes = Costume.query.all()
    return render_template('all_costumes.html', costumes=all_costumes, total=total)

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
    return render_template('blm.html', links=links, link_cat=link_cat)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
