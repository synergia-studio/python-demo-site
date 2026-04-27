from flask import Flask, jsonify, request

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
    with Session() as session:
        # Loop through every input field submitted
        print(f"Form Data: {request.form.items()}")
        
        for key, value in request.form.items():
            print(f"Field: {key} | Value: {value}")
            
        print(f"Check your terminal to see the loop output!")
        
        try:
            new_contact_us = ContactUs(client_ip = request.form.get('client_ip'),
                                       first_name = request.form.get('first_name'),
                                       last_name = request.form.get('last_name'),
                                       email = request.form.get('email'),
                                       subject = request.form.get('subject'),
                                       message = request.form.get('subject')
                                      )
            session.add(new_contact_us)
            session.commit()
            # SQLAlchemy automatically updates the object
            print(f"The new ID is: {new_contact_us.id}")
        except Exception as e:
            session.rollback()  # Undo the 'add' so the session isn't stuck
            print(f"Error: {e}")
        finally:
            session.close()
    # insertId = cursor.lastrowid
    # applyById(insertId);
    return 1 # insertId
