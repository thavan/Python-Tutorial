import os
import config
import pickle
import uuid


class Contact:
    def __init__(self, id, first_name, last_name, phone_numbers, email, **other_info):
        if id is None:
            self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.phone_numbers = phone_numbers
        self.email = email
        self.other_info.extend(other_info)

    def __repr__(self):
        return self.contact_info.first_name, self.contact_info.last_name

    def save(self):
        save_string = pickle.dumps(self)
        with open(os.path.join(config.STORAGE_PATH, self.id + '.con'), 'w') as f:
            f.write(save_string)


class ContactManager():
    def __init__(self):
        self.contacts = []

    def read_contacts(self):
        contacts = []
        all_files = os.listdir(config.STORAGE_PATH)
        for f in all_files:
            with open(f) as cf:
                contact = pickle.loads(cf.read())
                contacts.append(contact)
        return contacts