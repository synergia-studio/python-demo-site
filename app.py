"""Importing os"""

import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine, BigInteger, String, Text, DateTime, Enum, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from controllers import about_us_controller, contact_us_controller, cv_controller
from controllers import home_controller, technologies_controller

# Load the .env files
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


# engine = create_engine("postgresql+psycopg://postgres:rakics98@localhost:5432/python_demo_site",
#                        echo = True,
#                        pool_pre_ping = True,  # Automatically checks if the connection is alive
#                        pool_size = 10,        # Keeps 10 connections ready to go
#                        max_overflow = 20)      # Allows 20 extra connections during heavy traffic)

# 1. Setup the Base and Engine
Base = declarative_base()

class ContactUsOrm(Base):
    """Defining class for sql table contact_us as ORM"""
    __tablename__ = "contact_us"
    id: Mapped[int] = mapped_column(BigInteger, primary_key = True, autoincrement = True)
    client_ip: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    first_name: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    last_name: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    email: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    subject: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable = True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable = True)
class UserStatus(Enum):
    """Defining class for sql table subscribers column roles"""
    ENABLED = '1'
    DISABLED = '2'
    DELETED = '3'
class UserRole(Enum):
    """Defining class for sql table subscribers column roles"""
    ADMIN = '1'
    CLIENT = '2'

class UserOrm(Base, UserStatus, UserRole):
    """Defining class for sql table users as ORM"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key = True, autoincrement = True)
    status: Mapped[int] = mapped_column(Integer, server_default=UserStatus.ENABLED,
                                        nullable = False)
    role: Mapped[int] = mapped_column(Integer, server_default = UserRole.CLIENT, nullable = False)
    first_name: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    last_name: Mapped[str] = mapped_column(String(255), server_default = '',
                                           nullable = False)
    email: Mapped[str] = mapped_column(String(255), server_default = '',
                                       nullable = False,  unique = True)
    password: Mapped[str] = mapped_column(String(255), server_default = '', nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable = True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable = True)
# 3. Create the table in the database
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

# from routes import home  # noqa: F401

app = Flask(__name__)

@app.route("/", methods=["GET"])
async def index():
    """Show home html page"""
    return home_controller.index()

@app.route("/home/", methods=["GET"])
async def home():
    """Show home html page"""
    return home_controller.index()

@app.route("/about-us/", methods=["GET"]) # , methods=["GET"]
async def about_us():
    """Show About Us html page"""
    return about_us_controller.index()

@app.route("/contact-us/", methods=["GET"])
def contact_us_index():
    """Show Contact Us form html page"""
    return contact_us_controller.index()

@app.route("/contact-us/", methods=["POST"])
def contact_us_create():
    """Create SQL insert data from Contact Us form submit html page"""
    with engine.connect() as db:
        html = contact_us_controller.create(session, ContactUsOrm)
        db.close()
    return html

@app.route("/contact-us/mail/<string:base64_json>", methods=["GET"])
def contact_us_mail(base64_json):
    """show web page with html Email popup after Contact Us form submit"""
    return contact_us_controller.mail(session, ContactUsOrm, base64_json)


@app.route("/contact-us/thank-you/", methods=["GET"])
def contact_us_thank_you():
    """show web page with Thank You message after Contact Us form submit"""
    return contact_us_controller.thank_you()

@app.route("/cv/", methods=["GET"])
def cv():
    """show web page with Cv documents"""
    return cv_controller.index()

@app.route("/technologies/", methods=["GET"])
def technologies():
    """show web page with Technologies used"""
    return technologies_controller.index()

if __name__ == '__main__':
    app.run(host='localhost', port=4949)
