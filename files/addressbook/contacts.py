import os
import config
import pickle
import uuid
import collections

class Contact(object):
    def __init__(self, id=None, first_name='', last_name='', phone_number='', 
                    dob=None, address='', email='', other_info=[]):
        if id is None:
            self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.dob = dob
        self.address = address
        self.other_info = other_info

    def __repr__(self):
        return self.first_name + ' ' + self.last_name

    def save(self):
        """Saves the contact in disk"""
        with open(os.path.join(config.STORAGE_PATH, self.id + '.obj'), 'wb') as f:
            pickle.dump(self, f)


class ContactManager():
    def __init__(self):
        self.contacts = {}
        self.read_contacts()

    def read_contacts(self):
        """Returns list of contacts. Contacts are in the
        form of dictionary."""
        self.contacts = {}
        all_files = os.listdir(config.STORAGE_PATH)
        for f in all_files:
            with open(os.path.join(config.STORAGE_PATH, f), 'rb') as cf:
                contact = pickle.load(cf)
                self.contacts[contact.id] = contact
        return self.contacts

if __name__ == '__main__':
    c = Contact(first_name='John', last_name='Smith')
    c.save()
    c = Contact(first_name='Thavanathan', last_name='Thangaraj')
    c.save()