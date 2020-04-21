from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func


app = Flask(__name__)

ENV = 'dev'

if ENV =='dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost/height_collector'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nxkgxujpzdplau:35a3df623627b98cc18924eff23693df11f3543a5dde21713201f0c38369ac30@ec2-54-147-209-121.compute-1.amazonaws.com:5432/dft5ujpe1glkda'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Data(db.Model):
    __tablename__="heightdata"
    id= db.Column(db.Integer, primary_key=True)
    name_ = db.Column(db.String(80), unique=True, nullable=False)
    email_= db.Column(db.String(120), unique=True, nullable=False)
    age_ = db.Column(db.Integer, nullable=False)
    height_= db.Column(db.Integer , nullable=False)

    def __init__(self,name_, email_, age_, height_):
        self.name_ = name_
        self.email_ = email_
        self.age_ = age_
        self.height_ = height_

# initialize the variable execute when u call the class


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        name=request.form["name_name"]
        age = request.form["age_name"]
        height = request.form["height_name"]
        #summit once
        if db.session.query(Data).filter(Data.email_ == email).count()== 0:
            data=Data(name,email,age,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            print(average_height)
            return render_template("success.html")
    return render_template('index.html', text="Seems like we got something from that email once!")


if __name__ == '__main__':
    app.run()



# python app.py