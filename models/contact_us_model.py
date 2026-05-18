import json
import base64
import traceback
from typing import Callable
from flask import Flask
from sqlalchemy import select, func

func: Callable = func

app = Flask(__name__)

def create(session, contact_us_orm, request):
    """Creates/Insert new Contact Us form values to database"""
    last_insert_id = 0
    with session() as session:
        try:
            new_contact_us = contact_us_orm(client_ip = request.remote_addr,
                                            first_name = request.form.get('first_name'),
                                            last_name = request.form.get('last_name'),
                                            email = request.form.get('email'),
                                            subject = request.form.get('subject'),
                                            message = request.form.get('message'),
                                            created_at = func.now()
                                     )
            session.add(new_contact_us)
            session.flush()
            last_insert_id = new_contact_us.id
            session.commit()
            print(f"=================== {last_insert_id} == {new_contact_us.id}")
        except Exception as e:
            # traceback.print_exc()
            print(f"Error at ContactUsModel.create(Session, contact_us_orm): {e}")
            session.rollback()  # Undo the 'add' so the session isn't stuck
        finally:
            session.close()
    return last_insert_id

def get_token(session, contact_us_orm, last_insert_id):
    """Gets base 64 token used in html mail popup"""
    base64_token = ""
    with session() as session:
        try:
            print(f"***************** {contact_us_orm.id} == {last_insert_id}")
            stmt = select(contact_us_orm).where(contact_us_orm.id == last_insert_id)
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
            session.rollback()
            print(f"Error at get_token(session, contact_us_orm, last_insert_id) {e}")
            # traceback.print_exc()
        finally:
            session.close()
    return base64_token

def apply_from_token(Session, contact_us_orm, base64_token):
    """Fetch from contact_us sql table row based on decoded base64_token values"""
    contact_us = {}
    with Session() as session:
        try:
            # 1. Convert Token back to Base64 Bytes
            # 2. Decode Base64 to JSON String
            decoded_json = base64.b64decode(base64_token).decode('utf-8')
            # 3. Parse JSON back to Dictionary
            contact_us_dictionary = json.loads(decoded_json)
            print(f"contact_us_dictionary = {contact_us_dictionary}")
            stmt = (select(contact_us_orm)
                    .where(contact_us_orm.id == contact_us_dictionary["id"])
                    .where(contact_us_orm.client_ip == contact_us_dictionary["client_ip"])
                    .where(contact_us_orm.first_name == contact_us_dictionary["first_name"])
                    .where(contact_us_orm.last_name == contact_us_dictionary["last_name"])
                    .where(contact_us_orm.email == contact_us_dictionary["email"]
                   )
            )
            contact_us = session.execute(stmt).scalar()
        except Exception as e:
            print(f"Error at ContactUsModel.apply_from_token(Session, contact_us_orm): {e}")
            traceback.print_exc()
        finally:
            session.close()
    return contact_us
