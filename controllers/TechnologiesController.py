from flask import Flask, render_template

app = Flask(__name__)

# GET /technologies/
def index():
    return render_template("technologies.html",
                            site_title = 'Technologies Page',
                            technologies_menu_link_active = 'active',
                            header_title = "Technologies",
                            main_section_title = 'Technologies'
                          )



