from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from contacts import ContactManager, Contact


class AddressBook(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        self.namelist_widget = QtWidgets.QListWidget()
        self.cm = ContactManager()

        for contact in self.cm.contacts.values():
            name = QtWidgets.QListWidgetItem()
            name.id = contact.id
            name.setText('{} {}'.format(contact.first_name, contact.last_name))
            self.namelist_widget.addItem(name)

        self.current_contact = None
        self.search_field = QtWidgets.QLineEdit()

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

        self.other_info_group_label = QtWidgets.QLabel("Other info:")
        self.other_info_name_label = QtWidgets.QLabel("Name:")
        self.other_info_name = QtWidgets.QLineEdit()
        self.other_info_value_label = QtWidgets.QLabel("Value:")
        self.other_info_value = QtWidgets.QLineEdit()

        self.new_address = QtWidgets.QPushButton("&New")
        self.save_button = QtWidgets.QPushButton("&Save")
        self.edit_button = QtWidgets.QPushButton("&Edit")
        self.new_other_button = QtWidgets.QPushButton('')
        self.new_other_button.setIcon(QIcon('icons\plus-5-16.ico'))

        self.extra_info_context_menu = None

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

        self.other_info_list_widget = QtWidgets.QListWidget()

        contact_info_layout.addWidget(self.other_info_group_label, 6, 0)
        contact_info_layout.addWidget(self.other_info_name_label, 7, 0)
        contact_info_layout.addWidget(self.other_info_name, 7, 1)
        contact_info_layout.addWidget(self.other_info_value_label, 8, 0)
        contact_info_layout.addWidget(self.other_info_value, 8, 1)
        contact_info_layout.addWidget(self.new_other_button, 8, 2)

        contact_info_layout.addWidget(self.other_info_list_widget, 9, 0, 1, 3)
        contact_info_layout.addWidget(self.save_button, 10, 1)

        # left panel contact list
        contact_list_layout = QtWidgets.QVBoxLayout()
        contact_list_layout.addWidget(self.search_field)
        contact_list_layout.addWidget(self.namelist_widget)
        contact_list_layout.addWidget(self.new_address)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(contact_list_layout, 0, 0)
        self.mainLayout.addLayout(contact_info_layout, 0, 1)

        # event handling
        self.namelist_widget.itemClicked.connect(self.name_selected)
        self.save_button.clicked.connect(self.save_contact)
        self.search_field.textChanged.connect(self.search_field_changed)
        self.new_other_button.clicked.connect(self.add_new_info)

        # right click delete info for other menu
        self.other_info_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.other_info_list_widget.customContextMenuRequested.connect(self.extra_info_right_clicked)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Address Book")

    def search_field_changed(self, text):
        for count in range(self.namelist_widget.count()):
            contact = self.namelist_widget.item(count)
            if contact.text().lower().find(text.lower()) == -1:
                print(contact.text(), text)
                contact.setHidden(True)
            else:
                contact.setHidden(False)

    def extra_info_right_clicked(self, pos):
        self.extra_info_context_menu = QtWidgets.QMenu()
        menu_item = self.extra_info_context_menu.addAction("Delete")
        menu_item.triggered.connect(self.remove_other_info_clicked)
        parent_position = self.other_info_list_widget.mapToGlobal(QPoint(0, 0))
        self.extra_info_context_menu.move(parent_position + pos)
        self.extra_info_context_menu.show()

    def remove_other_info_clicked(self):
        item = self.other_info_list_widget.selectedItems()[0]
        row = self.other_info_list_widget.row(item)
        self.other_info_list_widget.takeItem(row)
        del item

    def add_new_info(self):
        item = QtWidgets.QListWidgetItem()
        item.setText('{:<50}: {}'.format(self.other_info_name.text(), self.other_info_value.text()))
        self.other_info_list_widget.addItem(item)
        self.other_info_name.setText('')
        self.other_info_value.setText('')

    def name_selected(self, item):
        self.current_contact = self.cm.contacts[item.id]
        self.first_name.setText(self.current_contact.first_name)
        self.last_name.setText(self.current_contact.last_name)
        self.phone_number.setText(self.current_contact.phone_number)
        self.email.setText(self.current_contact.email)
        self.dob.setText(self.current_contact.dob)
        self.address.setText(self.current_contact.address)
        for count in range(self.other_info_list_widget.count()):
            self.other_info_list_widget.takeItem(count)
        for other_info in self.current_contact.other_info:
            item = QtWidgets.QListWidgetItem()
            item.setText('{:<50}: {}'.format(other_info[0], other_info[1]))
            self.other_info_list_widget.addItem(item)

    def save_contact(self):
        self.current_contact.first_name = self.first_name.text()
        self.current_contact.last_name = self.last_name.text()
        self.current_contact.phone_number = self.phone_number.text()
        self.current_contact.email = self.email.text()
        self.current_contact.dob = self.dob.text()
        self.current_contact.address = self.address.toPlainText()
        self.current_contact.other_info = []
        for i in range(self.other_info_list_widget.count()):
            other_info = self.other_info_list_widget.item(i)
            self.current_contact.other_info.append(tuple(other_info.text().split(':')))
        self.current_contact.save()

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
