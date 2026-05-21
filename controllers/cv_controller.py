"""Imports Flask"""
from flask import Flask, render_template

app = Flask(__name__)

# GET /cv/
def index():
    """Sends html CV page to browser"""
    return render_template("cv.html",
                            site_title = 'CV Page',
                            menu_tab_active = 'cv',
                            header_title = "CV",
                            main_section_title = 'Documents'
                          )
