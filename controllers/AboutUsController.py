from flask import Flask, render_template

app = Flask(__name__)

# GET /about-us/
def index():
    return render_template("about-us.html",
                            site_title = 'About Us Page',
                            about_menu_link_active = 'active',
                            header_title = "About Us",
                            main_section_title = 'About Us'
                           )


