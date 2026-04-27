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
def create(Session, ContactUsOrm, request):
    contact_us_model = ContactUsModel
    last_insert_id = contact_us_model.create(Session, ContactUsOrm, request);
    base64Json = contact_us_model.get_token(Session, ContactUsOrm, last_insert_id)
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

# GET /contact-us/mail/<base64_json>
def mail(Session, ContactUsOrm, base64_json):
    contact_us_model = ContactUsModel
    contact_us_model = contact_us_model.apply_from_token(Session, ContactUsOrm, base64_json);
    return render_template("contact-us-mail.html",
                           site_title = 'Contact Us email from ' + request.url_root + 'contact-us/',
                           contact_menu_link_active = 'active',
                           header_title = "Contact",
                           main_section_title = 'Contact Us',
                           root_url = request.url_root,
                           item = {
                                "id": contact_us_model.id,
                                "client_ip": contact_us_model.client_ip,
                                "first_name": contact_us_model.first_name,
                                "last_name": contact_us_model.last_name,
                                "email": contact_us_model.email,
                                "subject": contact_us_model.subject,
                                "message": contact_us_model.message,
                                "created_at": contact_us_model.created_at,
                                "updated_at": contact_us_model.updated_at
                            }
                        )
