from flask import Flask,render_template,request,redirect,url_for,flash
import os
from random import choice
import string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = os.urandom(24)

# SQLAlchemy Configuration and pass the application into SQLAlchemy class

basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# creating model/table
class ShortUrls(db.Model):
    __tablename__ = 'shorturls'
    id = db.Column(db.Integer,primary_key = True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    short_url = db.Column(db.String(500))

    
    def __init__(self, original_url,short_id,short_url):
        self.original_url = original_url
        self.short_id = short_id
        self.short_url = short_url

    def __repr__(self):
        return "original_url - {} short_id - {} short_url - {}".format(self.original_url, self.short_id,self.short_url)



def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        short_id = generate_short_id(8)
        url = request.form['url']
        short_url = request.host_url + short_id
        new_link = ShortUrls(original_url=url, short_id=short_id,short_url=short_url)
        db.session.add(new_link)
        db.session.commit()
        print("data added................")
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')


@app.route('/history')
def history():
    records = ShortUrls.query.all()
    return render_template('history.html',records=records)


@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

if(__name__) == '__main__':
    app.run(debug=True)
