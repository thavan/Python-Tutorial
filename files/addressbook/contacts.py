import os
import config
import pickle
import uuid


class Contact(object):
    def __init__(self, id=None, first_name='', last_name='', phone_number='', 
                    dob=None, address='', email='', other_info=[]):
        if id is None:
            self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.dob = dob
        self.address = address
        self.email = email
        self.other_info = other_info

    def __repr__(self):
        return self.first_name + ' ' + self.last_name

    def save(self):
        """Saves the contact in disk"""
        with open(os.path.join(config.STORAGE_PATH, str(self.id) + '.obj'), 'wb') as f:
            f.write(pickle.dumps(self))


class ContactManager():
    def __init__(self):
        self.contacts = []

    def read_contacts(self):
        """Returns list of contacts. Contacts are in the
        form of dictionary."""
        contacts = []
        all_files = os.listdir(config.STORAGE_PATH)
        for f in all_files:
            with open(os.path.join(config.STORAGE_PATH, f), 'rb') as cf:
                contact = pickle.loads(cf.read())
                contacts.append(contact)
        return contacts
