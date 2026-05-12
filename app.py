from flask import Flask, request
from sqlalchemy import create_engine, Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from controllers import AboutUsController, ContactUsController, CvController, TechnologiesController

# Load the .env file
load_dotenv()

# Access the variables
db_engine =  os.getenv("DB_ENGINE")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqldb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}",
    echo = True,
    pool_pre_ping = True,  # Automatically checks if the connection is alive
    pool_size = 10,        # Keeps 10 connections ready to go
    max_overflow = 20)      # Allows 20 extra connections during heavy traffic)


# engine = create_engine("postgresql+psycopg://postgres:rakics98@localhost:5432/python-demo-site",
#     echo = True,
#     pool_pre_ping = True,  # Automatically checks if the connection is alive
#     pool_size = 10,        # Keeps 10 connections ready to go
#     max_overflow = 20)      # Allows 20 extra connections during heavy traffic)

# 1. Setup the Base and Engine
Base = declarative_base()

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

# from routes import home  # noqa: F401

app = Flask(__name__)

@app.route("/", methods=["GET"])
async def index():
    from controllers import HomeController
    home_controller = HomeController
    return home_controller.index()

@app.route("/home/", methods=["GET"])
async def home():
    from controllers import HomeController
    home_controller = HomeController
    return home_controller.index()

@app.route("/about-us/", methods=["GET"]) # , methods=["GET"]
async def about_us():
    about_us_controller = AboutUsController 
    return about_us_controller.index() 
    
@app.route("/contact-us/", methods=["GET"])
def contact_us_index():
    contact_us_controller = ContactUsController
    return contact_us_controller.index()      

@app.route("/contact-us/", methods=["POST"])
def contact_us_create():
    contact_us_controller = ContactUsController
    with engine.connect() as db:
        html = contact_us_controller.create(Session, ContactUsOrm, request)
        db.close()
    return html 
   
@app.route("/contact-us/mail/<string:base64_json>", methods=["GET"])
def contact_us_mail(base64_json):
    contact_us_controller = ContactUsController
    return contact_us_controller.mail(Session, ContactUsOrm, base64_json)
   

@app.route("/contact-us/thank-you/", methods=["GET"])
def contact_us_thank_you():
    contact_us_controller = ContactUsController 
    return contact_us_controller.thank_you()

@app.route("/cv/", methods=["GET"])
def cv():
    cv_controller = CvController
    return cv_controller.index()
 
@app.route("/technologies/", methods=["GET"])
def technologies(): 
    technologies_controller = TechnologiesController
    return technologies_controller.index()   
    
if __name__ == '__main__':
    app.run(host='localhost', port=4949)
