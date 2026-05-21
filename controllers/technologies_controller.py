from flask import Flask, render_template

app = Flask(__name__)

# GET /technologies/
def index():
    """Flushes Technologies html page to browser"""
    return render_template("technologies.html",
                            site_title = 'Technologies Page',
                            menu_tab_active = 'technologies',
                            header_title = "Technologies",
                            main_section_title = 'Technologies'
                          )



