from flask import Flask, render_template

app = Flask(__name__)

# GET /cv/
def index():
    return render_template("cv.html",
                            site_title = 'CV Page',
                            cv_menu_link_active = 'active',
                            header_title = "CV",
                            main_section_title = 'Documents'
                          )



