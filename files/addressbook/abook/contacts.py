import os
import pickle
import uuid

from . import config

class Contact(object):
    def __init__(self, contact_id=None, first_name='', last_name='', phone_number='', 
                    dob=None, address='', email=''):
        if contact_id is None:
            self.contact_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.dob = dob
        self.address = address

    def __repr__(self):
        return self.first_name + ' ' + self.last_name

    def save(self):
        """Saves the contact in disk"""
        with open(os.path.join(config.STORAGE_PATH, self.contact_id + '.obj'), 'wb') as f:
            pickle.dump(self, f)

class ContactManager():
    def __init__(self):
        self.contacts = {}
        self.read_contacts()

    def read_contacts(self):
        """Returns list of contacts. Contacts are in the
        form of dictionary."""
        self.contacts = {}
        print(config.STORAGE_PATH)
        for f in os.listdir(config.STORAGE_PATH):
            path = os.path.join(config.STORAGE_PATH, f)
            if not os.path.isdir(path):
                with open(path, 'rb') as cf:
                    try:
                        contact = pickle.load(cf)
                        self.contacts[contact.contact_id] = contact
                    except (EOFError, pickle.UnpicklingError) as e:
                        print('Invalid file {} {}'.format(f, e))
        return self.contacts

def load_dummy_contacts():
    c = Contact(first_name='John', last_name='Smith')
    c.save()
    c = Contact(first_name='Thavanathan', last_name='Thangaraj')
    c.save()
    c = Contact(first_name='Areef')
    c.save()
    cm = ContactManager()
    print(cm.contacts)

