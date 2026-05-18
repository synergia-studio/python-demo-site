from flask import Flask, render_template

app = Flask(__name__)

# GET /home/ or GET / 
def index():
    return render_template("home.html",
                    site_title = 'Home page',
                    home_menu_link_active = 'active',
                    header_title = "Home",
                    main_section_title ='Introduction'
                    )

