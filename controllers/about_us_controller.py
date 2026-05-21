"""Imports Flask"""
from flask import Flask, render_template

app = Flask(__name__)

# GET /about-us/
def index():
    """Send About Us html page to browser"""
    return render_template("about-us.html",
                            site_title = 'About Us Page',
                            menu_tab_active = 'about_us',
                            header_title = "About Us",
                            main_section_title = 'About Us'
                           )
