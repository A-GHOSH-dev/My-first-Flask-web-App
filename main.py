from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import json
from datetime import datetime

local_server=True
with open('config.json','r') as c:
    params=json.load(c)["params"]
app = Flask(__name__)
app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail=Mail(app)

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri'] #mysql://root:@localhost/cleanblog'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

# sl_no , name , email , phn_num , message , date
class Contacts(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phn_num = db.Column(db.String(15), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)


@app.route("/")
def home():

    return render_template('index.html', params=params)

@app.route("/about")
def about():

    return render_template('about.html', params=params)


@app.route("/post")
def post():
    return render_template('post.html', params=params)

@app.route("/contact", methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        #add entry to database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

    # sl_no , name , email , phn_num , message , date
        entry=Contacts(name=name,email=email, phn_num=phone, date=datetime.now(), message=message)
        db.session.add(entry)
        db.session.commit()

        mail.send_message(subject='Hey there'+name,sender=email,recipients=[params['gmail-user']],body= message)

        '''def index():
            msg = Message("Hey there", sender=email, recipients=[params['gmail-user']])
            msg.body = message, phone
            mail.send(msg)
            return index()'''

    return render_template('contact.html', params=params)


app.run(debug=True)