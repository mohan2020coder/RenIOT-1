""" You are looking at the entire back-end code of the project. This may look
intimidating at first but if you break it into parts you will notice how simple a functionality
is defined which is later connected to another functionality and by these it becomes a big feature of the project.


TLDR:: The code is simple if you break it into parts and understand 1 function at a time.""" 


# We hope you installed all the dependencies the project requires 
# if not, please have a look at 'readme' file and follow the instructions

from flask import Flask, render_template, url_for, request, jsonify, g
from flask.helpers import flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required
from flask_wtf import FlaskForm
from sqlalchemy.orm import session
from flask.globals import session
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length
import hashlib
from datetime import datetime
from random import *
from flask_mail import *
from flask_mail import Message
from flask_mail import Mail
import pymysql


# The above imported modules are very necessary for the below written code to work
# It's better to leave it un-changed. if required you can import their modules for implementing the functionality

pymysql.install_as_MySQLdb()

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/infinosbox'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "shravanissshravanissshravaniss"

# The above code is for connecting the sql database to the backend
# so that the data can be transferred to and from the database.




app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'nreply760@gmail.com'
app.config['MAIL_PASSWORD'] = 'Vijay@26101996'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)

# The above code is use to implement a mail generating functionailty 
# for user-verification. nowadays this is very common.



db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user"


@login_manager.user_loader
def load_user(user_id):
    return Useruthentication.query.get(int(user_id))



""" Below is the code for defining the model or the abstraction version of defining the database.
Here a class is defined for every database and the column are the attributes of the class.
The class inherits from the model class of flask."""


class Useruthentication(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column('userID', db.Integer, primary_key=True)
    mailid = db.Column('mailID', db.String(20))
    userpassword = db.Column('userPassword', db.String(40))
    username = db.Column('userName', db.String(40))
    phno = db.Column('phno', db.Integer)
    rectym = db.Column('recentLogTym', db.DateTime)

    def __init__(self, mailid, userpassword, username, phno, rectym):
        self.mailid = mailid
        self.userpassword = userpassword
        self.username = username
        self.phno = phno
        self.rectym = rectym
"""The above class is written for defining the User table 
the user table consist of columns:
-----------------------------------------------------------
|id | mailid | userpassword |username| phno| recentLogTime|
|   |        |              |        |     |              |
|   |        |              |        |     |              |
|   |        |              |        |     |              |
-----------------------------------------------------------


"""

class Board(db.Model, UserMixin):
    __tablename__ = 'board'
    boardid = db.Column('boardID', db.Integer, primary_key=True)
    boardpassword = db.Column('boardPassword', db.String(33))
""" The Above class is written for creating a board database
     the table will look like this:
     --------------------------
     |boardID   | boardPassword|
     |          |              |
     |          |              |
     ---------------------------
"""


class WeatherData(db.Model, UserMixin):
    __tablename__ = 'weatherData'
    tempreature = db.Column('Tempreature', db.String(40))
    location = db.Column('Location', db.String(40))
    weatherdata = db.Column('weatherdata', db.String(40))

    def __init__(self, tempreature, location, weatherdata):
        self.tempreature = tempreature
        self.location = location
        self.weatherdata = weatherdata
"""The above class IS CREATED for modelling the Weather data table

    from this table the Weather data will be fetched. 
    ----------------------------------
    | Tempreature | Location | Weather|
    |             |          |        |
    |             |          |        |
    -----------------------------------

"""

# db.create_all()


""" The below defined classes are used to create html form s in a pyhtonic way.
it uses the FlaksForms and the module is already imported."""


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=12)], render_kw={"placeholder": "Username"})
    userpassword = PasswordField(validators=[InputRequired(), Length(min=5, max=12)],
                                 render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

""" This above class is used for creating the Login Form"""

class BoxLoginForm(FlaskForm):
    boardid = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Board-Id"})
    boardpassword = PasswordField(validators=[InputRequired(), Length(min=4, max=12)],
                                  render_kw={"placeholder": "Board-Password"})
    submit = SubmitField("Login")

""" This above class is used for creating the Box Login FORM""" 


class SignUpForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=12)], render_kw={"placeholder": "Username"})
    phno = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Phone No"})
    mailid = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mail-Id"})
    userpassword = PasswordField(validators=[InputRequired(), Length(min=5, max=12)],
                                 render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
""" This above class is used for creating the Sign Up form"""



# From here the Routing starts
# Routing defined in simple terms means to route the user to different pages of the web application
# Connecting the pages with each others and transferring data among pages and databases.

@app.route('/')
def home():
    return render_template('home.html')
# The route is for the HOME PAGE of the application



@app.route('/user', methods=["GET", "POST"])
def user():
    form = LoginForm()
    if form.validate_on_submit():
        us = hashlib.md5(form.username.data.encode())
        user = Useruthentication.query.filter_by(username=us.hexdigest()).first()
        md5 = hashlib.md5(form.userpassword.data.encode())
        if user and user.userpassword == md5.hexdigest():
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('user.html', form=form)


""" The above written Route is for the Login Process of the user.
    here the Login form created by flask forms class is displayed.
    The user will enter the credentials and that credentials are hashed using md5 function.
    now that hashed value is matched by the one stored in User table in the database.
    if the match is found then the user is re-directed to the Dashboard."""

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')
""" The above written route is to display the Dashboard """ 


"""
The below written Route is for the sign-up of the user. 
if the user is already a registered user then a Flash message will pop-up indicating the user is already registered.

in the second scemario if the user is new and is signing up for the first time then
the user will enter the credential some of which will get hashed using md5.
and the credential get stored in the newUser  Database
""" 

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        un = hashlib.md5(form.username.data.encode())
        up = hashlib.md5(form.userpassword.data.encode())
        user = Useruthentication.query.filter_by(username=un.hexdigest()).first()
        if user:
            flash("username already taken! Try again!", "info")
            return redirect(url_for('signup'))
        else:
            newUser = Useruthentication(username=un.hexdigest(),
                                        phno=form.phno.data,
                                        mailid=form.mailid.data,
                                        userpassword=up.hexdigest(),
                                        rectym=datetime.now())
            db.session.add(newUser)
            db.session.commit()
            flash("Registration successful", "info")
            return redirect(url_for('user'))

    return render_template('signup.html', form=form)


# @app.route('/userSignUp', methods=["POST"])
# def UserSignUp():
#     if request.method == 'POST':
#         data = request.get_json()
#         print(data['username'])
#         print(data['password'])
#         print(data['email'])
#         print(data['phoneno'])
#         return jsonify({"message": "signup"}), 200


"""
The below written code is for board login.
Logging to that the user will get access to the box
as always the credentials are hashed to provide a better security.
if the Credentials match a message will pop-up saying the login was successful"""




@app.route('/board', methods=["GET", "POST"])
@login_required
def board():
    form = BoxLoginForm()
    if form.validate_on_submit():
        user = Board.query.filter_by(boardid=form.boardid.data).first()
        md5 = hashlib.md5(form.boardpassword.data.encode())
        if user and user.boardpassword == md5.hexdigest():
            return "Box successfully logged in"
    return render_template('board.html', form=form)


""" The below written code is for the Sign-Up process for the box
The data is collected from the frontend in JSON format and is de-serialized and save din the database"""


@app.route('/boxSignUp', methods=["POST"])
def boardSignup():
    if request.method == 'POST':
        data = request.get_json()
        print(data['username'])
        print(data['password'])
        return jsonify({"message": "boxsignup"}), 200


# Forgot Password Functionality Goes From Here...
"""
If the user forgets the password then an email verification for resetting the password is done
The mail generating functionality is used here.
A mail is sent to the Mail id of the user which is stored in the database
this mail will contain some text and a six-digit number which is the OTP(one-time-password) 

if the mail id is wrong or not present then a danger message will flash
"""

@app.route('/Get_OTP', methods=['GET', 'POST'])
def Get_OTP():
    if request.method == "POST":
        useremail = request.form.get("user")
        result = Useruthentication.query.filter_by(mailid=useremail).first()
        if result is not None:
            session["user"] = useremail
            msg = Message('OTP', sender='nreply760@gmail.com', recipients=[result.mailid])
            msg.body = f"Hello {result.username} a request has been recieved to change the password for your Account your secret otp is \n {str(otp)}"
            mail.send(msg)
            flash(f"hello {result.username} otp has been sent you registered email id {result.mailid}", "success")
            return render_template("otp_valid.html")
        else:
            flash("UserName Does Not Exists", "danger")

    return render_template("reset.html")


"""
The below written code is for the submission of the OTP.
if the OTP does not matches with the one which was sent to the user's mail id
then a danger message will flash
"""


@app.route('/otp_validation', methods=['GET', 'POST'])
def otp_validation():
    if g.user:
        if request.method == "POST":
            user_otp = request.form.get("otp1")
            if user_otp == str(otp):
                return render_template("pw.html")
            else:
                flash("OTP doesn't Match", "danger")
                return render_template("otp_valid.html")



"""
The Below written code is for updating the password.
 the password is hashed before updating.
 after hashing it is stored into the database.
 and a message will flash indicating the password is successfully changed.
"""

@app.route('/Password_Update', methods=['GET', 'POST'])
def Password_Update():
    # Password encrypted Before Updating.
    if g.user:
        if request.method == "POST":
            ps = hashlib.md5(request.form.get("ps").encode())
            ps1 = hashlib.md5(request.form.get("ps1").encode())
            if ps.hexdigest() == ps1.hexdigest():
                Passwordupdate = Useruthentication.query.filter_by(mailid=g.user).first()
                print(Passwordupdate)
                Passwordupdate.userpassword = ps1.hexdigest()
                db.session.add(Passwordupdate)
                db.session.commit()
                flash("Password successfully change")
                return redirect(url_for('user'))
            else:
                flash("Password Doesnt Match", "danger")
                return redirect(url_for('Password_Update'))
        return render_template("pw.html")


@app.route('/userSignUp', methods=["POST"])
def UserSignUp():
    if request.method == 'POST':
        data = request.get_json()
        up = hashlib.md5(data['password'].encode())
        newUser = Useruthentication(username=data['username'],
                                    phno=data['phoneno'],
                                    mailid=data['email'],
                                    userpassword=up.hexdigest(),
                                    rectym=datetime.now())
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "signup"}), 200
    
@app.route('/boxSignUp', methods=["POST"])
def boardSignup():
    if request.method == 'POST':
        data = request.get_json()
        BoardUser = board(boardid = data['username'],boardpassword=data['password'])
        db.session.add(BoardUser)
        db.session.commit()
        return jsonify({"message": "boxsignup"}), 200

@app.route('/GetOtp', methods=['POST'])
def GetOtp():
    if request.method == 'POST':
        data = request.get_json()
        result = Useruthentication.query.filter_by(mailid=data['email']).first()
        if result is not None:
            session["user"] = data['email']
            msg = Message('OTP', sender='nreply760@gmail.com', recipients=[result.mailid])
            msg.body = f"Hello {result.username} a request has been recieved to change the password for your Account your secret otp is \n {str(otp)}"
            mail.send(msg)
            return jsonify({"message": "GetOtp"}), 200


@app.route('/OTP_validation', methods=['POST'])
def OTP_validation():
    if g.user:
        if request.method == "POST":
            data = request.get_json()
            if data['otp'] == str(otp):
                return jsonify({"message": "otp"}), 200





@app.route('/Reset_Password', methods=['POST'])
def Reset_Password():
    if g.user:
        if request.method == "POST":
            data = request.get_json()
            ps = hashlib.md5(data['password'].encode())
            ps2 = hashlib.md5(data['password2'].encode())
            if ps.hexdigest() == ps2.hexdigest():
                Passwordupdate = Useruthentication.query.filter_by(mailid=g.user).first()
                Passwordupdate.userpassword = ps2.hexdigest()
                db.session.add(Passwordupdate)
                db.session.commit()
                return jsonify({"message": 'Reset_Password'}), 200


# Created an temporary app route to display the WeatherData which get accessed from the weather table
@app.route('/weather', methods=['GET'])
def getWeatherData():
    return render_template("weather.html", wdata=WeatherData.query.all())




""" This route is created so that when the user set their custom tempreture
the tempreature is passed to the database and the box will react to the same
 also if the user Clicks on show recent tempreature then A message should flash
 showing the recent tempreature
 """
@app.route('/setTemp', methods=['POST'])
def setTempreature():
    if request.method=='POST':
        tempreature1=request.form.get('setTempField')
        db_temp=WeatherData.query.filter_by(id=1).first()
        dbtemp.tempreature=tempreature1
        db.session.commit()
        flash(f"The tempreature is set to {tempreature1}")

def showRecentTemp():
    t=WeatherData.query.filter_by(id=1).first()
    flash(f"The last Recorded tempreature is {t}")




@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]


if __name__ == "__main__":
    app.run(debug=True, port=5000)
