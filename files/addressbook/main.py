from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from contacts import ContactManager, Contact


class AddressBook(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        self.cm = ContactManager()
        # currently selected contact information
        self.current_contact = None

        # search field
        self.search_field = QtWidgets.QLineEdit()

        # name list
        self.namelist_widget = QtWidgets.QListWidget()
        for contact in self.cm.contacts.values():
            name = QtWidgets.QListWidgetItem()
            name.contact_id = contact.contact_id
            name.setText('{} {}'.format(contact.first_name, contact.last_name))
            self.namelist_widget.addItem(name)

        # button to create a new contact
        self.new_address = QtWidgets.QPushButton("&New")
        # left panel contact list
        contact_list_layout = QtWidgets.QVBoxLayout()
        contact_list_layout.addWidget(self.search_field)
        contact_list_layout.addWidget(self.namelist_widget)
        contact_list_layout.addWidget(self.new_address)

        # right side contact info
        self.first_name_label = QtWidgets.QLabel("First Name:")
        self.first_name = QtWidgets.QLineEdit()
        self.last_name_label = QtWidgets.QLabel("Last Name:")
        self.last_name = QtWidgets.QLineEdit()

        self.phone_number_label = QtWidgets.QLabel("Phone Number")
        self.phone_number = QtWidgets.QLineEdit()

        self.email_label = QtWidgets.QLabel("Email")
        self.email = QtWidgets.QLineEdit()

        self.dob_label = QtWidgets.QLabel("Date of birth")
        self.dob = QtWidgets.QLineEdit()

        self.address_label = QtWidgets.QLabel("Address:")
        self.address = QtWidgets.QTextEdit()

        self.save_button = QtWidgets.QPushButton("&Save")

        contact_info_layout = QtWidgets.QGridLayout()
        contact_info_layout.addWidget(self.first_name_label, 0, 0)
        contact_info_layout.addWidget(self.first_name, 0, 1)
        contact_info_layout.addWidget(self.last_name_label, 1, 0)
        contact_info_layout.addWidget(self.last_name, 1, 1)
        contact_info_layout.addWidget(self.phone_number_label, 2, 0)
        contact_info_layout.addWidget(self.phone_number, 2, 1)
        contact_info_layout.addWidget(self.email_label, 3, 0)
        contact_info_layout.addWidget(self.email, 3, 1)
        contact_info_layout.addWidget(self.dob_label, 4, 0)
        contact_info_layout.addWidget(self.dob, 4, 1)

        contact_info_layout.addWidget(self.address_label, 5, 0, Qt.AlignTop)
        contact_info_layout.addWidget(self.address, 5, 1)
        contact_info_layout.addWidget(self.save_button, 6, 1)


        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(contact_list_layout, 0, 0)
        self.mainLayout.addLayout(contact_info_layout, 0, 1)

        # event handling
        self.namelist_widget.itemClicked.connect(self.name_selected)
        self.save_button.clicked.connect(self.save_contact)
        self.search_field.textChanged.connect(self.search_field_changed)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Address Book")

    def search_field_changed(self, search_text):
        for count in range(self.namelist_widget.count()):
            contact_list_item = self.namelist_widget.item(count)
            list_text = contact_list_item.text().lower() # find the selected text
            if list_text.find(search_text.lower()) == -1:
                contact_list_item.setHidden(True)
            else:
                contact_list_item.setHidden(False)


    def name_selected(self, item):
        self.current_contact = self.cm.contacts[item.contact_id]
        self.first_name.setText(self.current_contact.first_name)
        self.last_name.setText(self.current_contact.last_name)
        self.phone_number.setText(self.current_contact.phone_number)
        self.email.setText(self.current_contact.email)
        self.dob.setText(self.current_contact.dob)
        self.address.setText(self.current_contact.address)

    def save_contact(self):
        self.current_contact.first_name = self.first_name.text()
        self.current_contact.last_name = self.last_name.text()
        self.current_contact.phone_number = self.phone_number.text()
        self.current_contact.email = self.email.text()
        self.current_contact.dob = self.dob.text()
        self.current_contact.address = self.address.toPlainText()
        self.current_contact.save()

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
