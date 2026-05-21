from flask import Flask, render_template, jsonify, request
from models import contact_us_model

app = Flask(__name__)

# GET /contact-us/
def index():
    """Flushes to browser Contact Us page with form to fill"""
    return render_template("contact-us-form.html",
                            site_title = 'Contact Us Page',
                            menu_tab_active = 'contact_us',
                            header_title = "Contact",
                            main_section_title = 'Contact Us'
                           )

# POST /contact-us/
def create(session, contact_us_orm):
    """"Create/Insert Contact Us form values"""
    last_insert_id = contact_us_model.create(session, contact_us_orm, request)
    base_64_json = contact_us_model.get_token(session, contact_us_orm, last_insert_id)
    json = {
        "success": True,
        "message": 'Saved successfully',
        "thank_you_url": request.url_root + 'contact-us/thank-you',
        "redirect": request.url_root + 'contact-us/mail/' + base_64_json
    }
    return jsonify(json)

# GET /contact-us/thank-you/
def thank_you():
    """Flushes to browser thank you page after Contact US form submit"""
    return render_template("contact-us-thank-you.html",
                            site_title = 'Contact Us Thank You Page',
                            menu_tab_active = 'contact_us',
                            header_title = "Contact",
                            main_section_title = 'Contact Us'
                           )

# GET /contact-us/mail/<base64_json>
def mail(session, contact_us_orm, base64_json):
    """Creates html email for popup of Contact Us for submit"""
    model = contact_us_model.apply_from_token(session, contact_us_orm, base64_json)
    return render_template("contact-us-mail.html",
                           site_title = 'Contact Us email from ' + request.url_root + 'contact-us/',
                           header_title = "Contact",
                           main_section_title = 'Contact Us',
                           root_url = request.url_root,
                           item = {
                                "id": model.id,
                                "client_ip": model.client_ip,
                                "first_name": model.first_name,
                                "last_name": model.last_name,
                                "email": model.email,
                                "subject": model.subject,
                                "message": model.message,
                                "created_at": model.created_at,
                                "updated_at": model.updated_at
                            }
                        )
