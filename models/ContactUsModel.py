from flask import Flask, jsonify, request
import datetime
from sqlalchemy import select
import json
import base64

app = Flask(__name__)

columns = { 
    "id": 0,
    "client_ip": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "subject": "",
    "message": "",
    "created_at": "0000-00-00 00:00:00",
    "updated_at": "0000-00-00 00:00:00"
}

# json = request.get_json()
def apply_from_json(json):
    columns["client_ip"] = json.client_ip;
    columns["first_name"] = json.firstname;
    columns["last_name"] = json.lastname;
    columns["email"] = json.email;
    columns["subject"] = json.subject;
    columns["message"] = json.message;

def create(Session, ContactUs, request):
    last_insert_id = 0
    with Session() as session:
        # for key, value in request.form.items():
        #    print(f"Field: {key} | Value: {value}")
        try:
            new_contact_us = ContactUs(client_ip = request.remote_addr,
                                    first_name = request.form.get('first_name'),
                                    last_name = request.form.get('last_name'),
                                    email = request.form.get('email'),
                                    subject = request.form.get('subject'),
                                    message = request.form.get('message'),
                                    created_at = datetime.datetime.now()
                                    )
            session.add(new_contact_us)
            session.commit()
            last_insert_id = new_contact_us.id 
        except Exception as e:
            session.rollback()  # Undo the 'add' so the session isn't stuck
            print(f"Error at ContactUsModel.create(Session, ContactUs, request): {e}")
        finally:
            session.close()
    return last_insert_id

def get_token(Session, ContactUs, last_insert_id):
    base64_token = ""
    with Session() as session:
        try:
            stmt = select(ContactUs).where(ContactUs.id == last_insert_id)
            contact_us = session.execute(stmt).scalar()
            
            data = {"id": contact_us.id, 
                    "client_ip": contact_us.client_ip,
                    "first_name": contact_us.first_name,
                    "last_name": contact_us.last_name,
                    "email": contact_us.email
                   }
            # 1. Convert Dictionary to JSON String
            json_string = json.dumps(data)
            # 2. Convert String to Bytes, then to Base64 Bytes
            # .encode() turns string to bytes
            # b64encode() creates the base64 version
            base64_bytes = base64.b64encode(json_string.encode('utf-8'))
            # 3. Convert Bytes back to a String Token
            base64_token = base64_bytes.decode('utf-8')
        except Exception as e:
            print(f"Error at ContactUsModel.get_token(Session, ContactUs, last_insert_id): {e}")
        finally:
            session.close()
    return base64_token

def apply_from_token(Session, ContactUs, base64_token):
    contact_us_model = ContactUs
    with Session() as session:
        try:
            # 1. Convert Token back to Base64 Bytes
            # 2. Decode Base64 to JSON String
            decoded_json = base64.b64decode(base64_token).decode('utf-8')
            # 3. Parse JSON back to Dictionary
            contact_us_dictionary = json.loads(decoded_json)
            stmt = select(ContactUs).where(ContactUs.id == contact_us_dictionary.id,
                                           ContactUs.client_ip == contact_us_dictionary.client_ip,
                                           ContactUs.first_name == contact_us_dictionary.first_name,
                                           ContactUs.last_name == contact_us_dictionary.last_name,
                                           ContactUs.email == contact_us_dictionary.email
                                          )
            contact_us_model = session.execute(stmt).scalar()
            print("----------------------")
            print(session.get(contact_us_model, 1))
        except Exception as e:
            print(f"Error at ContactUsModel.get_token(Session, ContactUs, last_insert_id): {e}")
        finally:
            session.close()
    return contact_us_model
