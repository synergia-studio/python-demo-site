from flask import Flask, render_template, jsonify, request
from models import ContactUsModel

app = Flask(__name__)

# GET /contact-us/
def index():
    return render_template("contact-us-form.html",
                            site_title = 'Contact Us Page',
                            contact_menu_link_active = 'active',
                            header_title = "Contact",
                            main_section_title = 'Contact Us'
                            )

# POST /contact-us/
def create(Session, ContactUs, request):
    contact_us = ContactUsModel
    # this.req.body.client_ip = this.req.ip.replace('::ffff:', '');
    # contact_us.apply_from_json(request.get_json());
    lastInsertId = contact_us.create(Session, ContactUs, request);
    # contact_us.applyById(lastInsertId);
    # base64Json = contact_us.getToken(lastInsertId);
    base64Json = "1234567890"
    json = {
        "success": True,
        "message": 'Saved successfully',
        "thank_you_url": request.url_root + 'contact-us/thank-you',
        "redirect": request.url_root + 'contact-us/mail/' + base64Json
    }
    return jsonify(json)

# GET /contact-us/thank-you/
def thank_you():
    return render_template("contact-us-thank-you.html",
                            site_title = 'Contact Us Thank You Page',
                            contact_menu_link_active = 'active',
                            header_title = "Contact",
                            main_section_title = 'Contact Us'
                            )

# GET /contact-us/mail/<base64Json>
def mail(base64Json):
    base64Json = base64Json
    # const ContactUsModel = require('../models/ContactUsModel');
    # const contactUs =  new ContactUsModel(this.db);
    # var item = await contactUs.applyFromToken(base64Json);
    return render_template("contact-us-mail.html",
                            site_title = 'Contact Us email from ' + request.url_root + 'contact-us/',
                            contact_menu_link_active = 'active',
                            header_title = "Contact",
                            main_section_title = 'Contact Us',
                            root_url = request.url_root,
                            item = {}
                        )
