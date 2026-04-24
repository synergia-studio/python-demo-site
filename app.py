from flask import Flask,render_template , request

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python-demo-site',
        'USER': 'root',
        'PASSWORD': 'rakics98',
        'HOST': 'localhost',      # Or your database IP address
        'PORT': '3306',           # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

app = Flask(__name__) #initializing flask

@app.route("/", methods=["GET"])
def index():
    from controllers import HomeController
    homeCtrl = HomeController
    return homeCtrl.index()

@app.route("/home/", methods=["GET"])
def home():
    from controllers import HomeController
    homeCtrl = HomeController
    return homeCtrl.index()


@app.route("/about-us/", methods=["GET"])
def about_us():
    from controllers import AboutUsController
    aboutUsCtrl = AboutUsController 
    return aboutUsCtrl.index() 
    
@app.route("/contact-us/", methods=["GET"])
def contact_us_index():
    from controllers import ContactUsController
    contactUsCtrl = ContactUsController # The `ContactUsController` is a controller class that likely handles the logic
    # and functionality related to the contact us feature of the web application.
    # Based on the route definitions in the code snippet provided, the
    # `ContactUsController` class seems to contain methods for displaying the contact
    # us form, creating a new contact entry, sending an email with contact
    # information, and displaying a thank you message after submitting the contact
    # form.
    # The `ContactUsController` is a controller class that likely handles the logic
    # and functionality related to the contact us section of the web application. It
    # contains methods such as `index()`, `create()`, `mail(base64Json)`, and
    # `thank_you()` which are responsible for handling different actions related to
    # the contact us feature.
    return contactUsCtrl.index()      

@app.route("/contact-us/", methods=["POST"])
def contact_us_create():
    from controllers import ContactUsController
    contactUsCtrl = ContactUsController
    return contactUsCtrl.create()
   
@app.route("/contact-us/mail/<base64Json>", methods=["GET"])
def contact_us_mail(base64Json):
    from controllers import ContactUsController
    contactUsCtrl = ContactUsController
    return contactUsCtrl.mail(base64Json)
   

@app.route("/contact-us/thank-you/", methods=["GET"])
def contact_us_thank_you():
    from controllers import ContactUsController
    contactUsCtrl = ContactUsController 
    return contactUsCtrl.thank_you()

@app.route("/cv/", methods=["GET"])
def cv():
    from controllers import CvController
    cvCtrl = CvController
    return cvCtrl.index()
 
@app.route("/technologies/", methods=["GET"])
def technologies(): 
    from controllers import TechnologiesController
    technologiesCtrl = TechnologiesController
    return technologiesCtrl.index()   
    
# @app.route("/") #defining the routes for the home() function (Multiple routes can be used as seen here)
# @app.route("/home")
# def home():
#     return render_template("home.html") #rendering our home.html contained within /templates

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
