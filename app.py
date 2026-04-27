from flask import Flask,render_template , request
from sqlalchemy import create_engine, Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from controllers import ContactUsController

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python-demo-site',
        'USER': 'root',
        'PASSWORD': 'rakics98',
        'HOST': 'localhost',      # Or your database IP address
        'PORT': '3306',           # Default MySQL port
        'OPTIONsS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

engine = create_engine("mysql+mysqldb://root:rakics98@localhost/python-demo-site",
    echo = True,
    pool_pre_ping = True,  # Automatically checks if the connection is alive
    pool_size = 10,        # Keeps 10 connections ready to go
    max_overflow = 20)      # Allows 20 extra connections during heavy traffic)

# 2. Define the Table Structure (The Model)
class Base(DeclarativeBase):
    pass

class ContactUsOrm(Base):
    __tablename__ = "contact_us"
    id = Column(BigInteger, primary_key = True, autoincrement = True, unique = True)
    client_ip = Column(String(255), nullable = False, default = '')
    first_name = Column(String(255), nullable = False, default = '')
    last_name = Column(String(255), nullable = False, default = '')    
    email = Column(String(255), nullable = False, default = '') 
    subject = Column(String(255), nullable = False, default = '') 
    message = Column(Text)
    created_at = Column(DateTime, default = '0000-00-00 00:00:00')
    updated_at = Column(DateTime, default = '0000-00-00 00:00:00') 

# 3. Create the table in the database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

app = Flask(__name__) #initializing flask

@app.route("/", methods=["GET"])
def index():
    from controllers import HomeController
    home = HomeController
    return home.index()

@app.route("/home/", methods=["GET"])
def home():
    from controllers import HomeController
    home = HomeController
    return home.index()


@app.route("/about-us/", methods=["GET"])
def about_us():
    from controllers import AboutUsController
    about_us = AboutUsController 
    return about_us.index() 
    
@app.route("/contact-us/", methods=["GET"])
def contact_us_index():
    contact_us = ContactUsController
    return contact_us.index()      

@app.route("/contact-us/", methods=["POST"])
def contact_us_create():
    contact_us = ContactUsController
    with engine.connect() as db:
        html = contact_us.create(Session, ContactUsOrm, request)
        db.close()
    return html 
   
@app.route("/contact-us/mail/<string:base64_json>", methods=["GET"])
def contact_us_mail(base64_json):
    contact_us = ContactUsController
    return contact_us.mail(Session, ContactUsOrm, base64_json)
   

@app.route("/contact-us/thank-you/", methods=["GET"])
def contact_us_thank_you():
    contact_us = ContactUsController 
    return contact_us.thank_you()

@app.route("/cv/", methods=["GET"])
def cv():
    from controllers import CvController
    cv = CvController
    return cv.index()
 
@app.route("/technologies/", methods=["GET"])
def technologies(): 
    from controllers import TechnologiesController
    technologies = TechnologiesController
    return technologies.index()   
    
@app.route("/account", methods=["POST", "GET"]) #defining the routes for the account() funtion
def account():
    usr = "<User Not Defined>" #Creating a variable usr
    if (request.method == "POST"): #Checking if the method of request was post
        usr = request.form["name"] #getting the name of the user from the form on home page
        if not usr: #if name is not defined it is set to default string
            usr = "<User Not Defined>"
    return render_template("account.html",username=usr) #rendering our account.html contained within /templates



if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True,port=4949) #running flask (Initialized on line 4)
