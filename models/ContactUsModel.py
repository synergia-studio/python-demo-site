from flask import Flask, jsonify, request
from sqlalchemy import select, func
import json
import base64
import traceback

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

def create(Session, ContactUsOrm, request):
    last_insert_id = 0
    with Session() as session:
        try:
            new_contact_us = ContactUsOrm(client_ip = request.remote_addr,
                                      first_name = request.form.get('first_name'),
                                      last_name = request.form.get('last_name'),
                                      email = request.form.get('email'),
                                      subject = request.form.get('subject'),
                                      message = request.form.get('message'),
                                      created_at = func.now()
                                     )
            session.add(new_contact_us)
            session.commit()
            last_insert_id = new_contact_us.id 
        except Exception as e:
            session.rollback()  # Undo the 'add' so the session isn't stuck
            traceback.print_exc()
            print(f"Error at ContactUsModel.create(Session, ContactUsOrm, request): {e}")
        finally:
            session.close()
    return last_insert_id

def get_token(Session, ContactUsOrm, last_insert_id):
    base64_token = ""
    with Session() as session:
        try:
            stmt = select(ContactUsOrm).where(ContactUsOrm.id == last_insert_id)
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
            print(f"Error at ContactUsModel.get_token(Session, ContactUsOrm, last_insert_id): {e}")
            traceback.print_exc()
        finally:
            session.close()
    return base64_token

def apply_from_token(Session, ContactUsOrm, base64_token):
    contact_us = {}
    with Session() as session:
        try:
            # 1. Convert Token back to Base64 Bytes
            # 2. Decode Base64 to JSON String
            decoded_json = base64.b64decode(base64_token).decode('utf-8')
            # 3. Parse JSON back to Dictionary
            contact_us_dictionary = json.loads(decoded_json)
            print(f"contact_us_dictionary = {contact_us_dictionary}")
            stmt = (select(ContactUsOrm)
                    .where(ContactUsOrm.id == contact_us_dictionary["id"])
                    .where(ContactUsOrm.client_ip == contact_us_dictionary["client_ip"])
                    .where(ContactUsOrm.first_name == contact_us_dictionary["first_name"])
                    .where(ContactUsOrm.last_name == contact_us_dictionary["last_name"])
                    .where(ContactUsOrm.email == contact_us_dictionary["email"]
                   )
            )
            contact_us = session.execute(stmt).scalar()
        except Exception as e:
            print(f"Error at ContactUsModel.apply_from_token(Session, ContactUsOrm, last_insert_id): {e}")
            traceback.print_exc()
        finally:
            session.close()
    return contact_us
