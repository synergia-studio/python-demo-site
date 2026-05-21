from flask import Flask, render_template

app = Flask(__name__)

# GET /home/ or GET / 
def index():
    return render_template("home.html",
                    site_title = 'Home page',
                    menu_tab_active = 'home',
                    header_title = "Home",
                    main_section_title ='Introduction'
                    )

