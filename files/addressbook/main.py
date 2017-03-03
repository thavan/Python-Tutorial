import pickle

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout,
        QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
        QWidget, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QIcon

from contacts import ContactManager


class AddressBook(QWidget):
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)
        self.contact_id = None
        self.phone_numbers = []
        self.other_fields = []

        namelist_widget = QListWidget()
        self.cm = ContactManager()

        for contact in self.cm.read_contacts():
            name = QListWidgetItem()
            name.setText('{} {}'.format(contact.first_name, contact.last_name))
            namelist_widget.addItem(name)

        self.search_edit = QLineEdit()

        self.contact_info_empty = QLabel('Select a contact to view details')
        self.first_name_label = QLabel("First Name:")
        self.first_name = QLineEdit()
        self.last_name_label = QLabel("Last Name:")
        self.last_name = QLineEdit()

        self.other_info_group_label = QLabel("Other info:")
        self.other_info_name_label = QLabel("Name:")
        self.other_info_name = QLineEdit()
        self.other_info_value_label = QLabel("Value:")
        self.other_info_value = QLineEdit()

        self.phone_number_label = QLabel("Phone Number")
        self.phone_number = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address = QTextEdit()

        self.new_address = QPushButton("&New")
        self.save_button = QPushButton("&Save")
        self.edit_button = QPushButton("&Edit")
        self.new_other_button = QPushButton('')
        self.new_other_button.setIcon(QIcon('icons\plus-5-16.ico'))
        self.new_other_button.clicked.connect(self.add_new_info)

        contactLayout = QGridLayout()
        contactLayout.addWidget(self.first_name_label, 0, 0)
        contactLayout.addWidget(self.first_name, 0, 1)
        contactLayout.addWidget(self.last_name_label, 1, 0)
        contactLayout.addWidget(self.last_name, 1, 1)
        contactLayout.addWidget(self.phone_number_label, 2, 0)
        contactLayout.addWidget(self.phone_number, 2, 1)
        contactLayout.addWidget(self.address_label, 3, 0, Qt.AlignTop)
        contactLayout.addWidget(self.address, 3, 1)
        self.other_info_list = QListWidget()

        contactLayout.addWidget(self.other_info_group_label, 4, 0)
        contactLayout.addWidget(self.other_info_name_label, 6, 0)
        contactLayout.addWidget(self.other_info_name, 6, 1)
        contactLayout.addWidget(self.other_info_value_label, 7, 0)
        contactLayout.addWidget(self.other_info_value, 7, 1)

        contactLayout.addWidget(self.new_other_button, 7, 2)

        for other_info in [('Thavanathan', 'Thangaraj'), ('John', 'Smith')]:
            item = QListWidgetItem()
            item.setText('{}: {}'.format(other_info[0], other_info[1]))
            self.other_info_list.addItem(item)
        contactLayout.addWidget(self.other_info_list, 8, 0, 1, 3)

        contactLayout.addWidget(self.save_button, 9, 1)

        contact_list_layout = QVBoxLayout()
        contact_list_layout.addWidget(self.search_edit)
        contact_list_layout.addWidget(namelist_widget)
        contact_list_layout.addWidget(self.new_address)

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(contact_list_layout, 0, 0)
        self.mainLayout.addLayout(contactLayout, 0, 1)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("Simple Address Book")

    def add_new_info(self):
        item = QListWidgetItem()
        item.setText('{}: {}'.format(self.other_info_name.text(), self.other_info_value.text()))
        self.other_info_list.addItem(item)

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.updateInterface(self.AddingMode)

    def editContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.updateInterface(self.EditingMode)

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QMessageBox.information(self, "Empty Field",
                    "Please enter a name and address.")
            return

        if self.currentMode == self.AddingMode:
            if name not in self.contacts:
                self.contacts[name] = address
                QMessageBox.information(self, "Add Successful",
                        "\"%s\" has been added to your address book." % name)
            else:
                QMessageBox.information(self, "Add Unsuccessful",
                        "Sorry, \"%s\" is already in your address book." % name)
                return

        elif self.currentMode == self.EditingMode:
            if self.oldName != name:
                if name not in self.contacts:
                    QMessageBox.information(self, "Edit Successful",
                            "\"%s\" has been edited in your address book." % self.oldName)
                    del self.contacts[self.oldName]
                    self.contacts[name] = address
                else:
                    QMessageBox.information(self, "Edit Unsuccessful",
                            "Sorry, \"%s\" is already in your address book." % name)
                    return
            elif self.oldAddress != address:
                QMessageBox.information(self, "Edit Successful",
                        "\"%s\" has been edited in your address book." % name)
                self.contacts[name] = address

        self.updateInterface(self.NavigationMode)

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)
        self.updateInterface(self.NavigationMode)

    def removeContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name in self.contacts:
            button = QMessageBox.question(self, "Confirm Remove",
                    "Are you sure you want to remove \"%s\"?" % name,
                    QMessageBox.Yes | QMessageBox.No)

            if button == QMessageBox.Yes:
                self.previous()
                del self.contacts[name]

                QMessageBox.information(self, "Remove Successful",
                        "\"%s\" has been removed from your address book." % name)

        self.updateInterface(self.NavigationMode)

    def next(self):
        name = self.nameLine.text()
        it = iter(self.contacts)

        try:
            while True:
                this_name, _ = it.next()

                if this_name == name:
                    next_name, next_address = it.next()
                    break
        except StopIteration:
            next_name, next_address = iter(self.contacts).next()

        self.nameLine.setText(next_name)
        self.addressText.setText(next_address)

    def previous(self):
        name = self.nameLine.text()

        prev_name = prev_address = None
        for this_name, this_address in self.contacts:
            if this_name == name:
                break

            prev_name = this_name
            prev_address = this_address
        else:
            self.nameLine.clear()
            self.addressText.clear()
            return

        if prev_name is None:
            for prev_name, prev_address in self.contacts:
                pass

        self.nameLine.setText(prev_name)
        self.addressText.setText(prev_address)

    def findContact(self):
        self.dialog.show()

        if self.dialog.exec_() == QDialog.Accepted:
            contactName = self.dialog.getFindText()

            if contactName in self.contacts:
                self.nameLine.setText(contactName)
                self.addressText.setText(self.contacts[contactName])
            else:
                QMessageBox.information(self, "Contact Not Found",
                        "Sorry, \"%s\" is not in your address book." % contactName)
                return

        self.updateInterface(self.NavigationMode)

    def updateInterface(self, mode):
        self.currentMode = mode

        if self.currentMode in (self.AddingMode, self.EditingMode):
            self.nameLine.setReadOnly(False)
            self.nameLine.setFocus(Qt.OtherFocusReason)
            self.addressText.setReadOnly(False)

            self.addButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)

            self.nextButton.setEnabled(False)
            self.previousButton.setEnabled(False)

            self.submitButton.show()
            self.cancelButton.show()

            self.loadButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.exportButton.setEnabled(False)

        elif self.currentMode == self.NavigationMode:
            if not self.contacts:
                self.nameLine.clear()
                self.addressText.clear()

            self.nameLine.setReadOnly(True)
            self.addressText.setReadOnly(True)
            self.addButton.setEnabled(True)

            number = len(self.contacts)
            self.editButton.setEnabled(number >= 1)
            self.removeButton.setEnabled(number >= 1)
            self.findButton.setEnabled(number > 2)
            self.nextButton.setEnabled(number > 1)
            self.previousButton.setEnabled(number >1 )

            self.submitButton.hide()
            self.cancelButton.hide()

            self.exportButton.setEnabled(number >= 1)

            self.loadButton.setEnabled(True)
            self.saveButton.setEnabled(number >= 1)

    def saveToFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Address Book",
                '', "Address Book (*.abk);;All Files (*)")

        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return

        pickle.dump(self.contacts, out_file)
        out_file.close()

    def loadFromFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Address Book",
                '', "Address Book (*.abk);;All Files (*)")

        if not fileName:
            return

        try:
            in_file = open(str(fileName), 'rb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                    "There was an error opening \"%s\"" % fileName)
            return

        self.contacts = pickle.load(in_file)
        in_file.close()

        if len(self.contacts) == 0:
            QMessageBox.information(self, "No contacts in file",
                    "The file you are attempting to open contains no "
                    "contacts.")
        else:
            for name, address in self.contacts:
                self.nameLine.setText(name)
                self.addressText.setText(address)

        self.updateInterface(self.NavigationMode)

    def exportAsVCard(self):
        name = str(self.nameLine.text())
        address = self.addressText.toPlainText()

        nameList = name.split()

        if len(nameList) > 1:
            firstName = nameList[0]
            lastName = nameList[-1]
        else:
            firstName = name
            lastName = ''

        fileName, _ = QFileDialog.getSaveFileName(self, "Export Contact", '',
                "vCard Files (*.vcf);;All Files (*)")

        if not fileName:
            return

        out_file = QFile(fileName)

        if not out_file.open(QIODevice.WriteOnly):
            QMessageBox.information(self, "Unable to open file",
                    out_file.errorString())
            return

        out_s = QTextStream(out_file)

        out_s << 'BEGIN:VCARD' << '\n'
        out_s << 'VERSION:2.1' << '\n'
        out_s << 'N:' << lastName << ';' << firstName << '\n'
        out_s << 'FN:' << ' '.join(nameList) << '\n'

        address.replace(';', '\\;')
        address.replace('\n', ';')
        address.replace(',', ' ')

        out_s << 'ADR;HOME:;' << address << '\n'
        out_s << 'END:VCARD' << '\n'

        QMessageBox.information(self, "Export Successful",
                "\"%s\" has been exported as a vCard." % name)


class FindDialog(QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        findLabel = QLabel("Enter the name of a contact:")
        self.lineEdit = QLineEdit()

        self.findButton = QPushButton("&Find")
        self.findText = ''

        layout = QHBoxLayout()
        layout.addWidget(findLabel)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.findButton)

        self.setLayout(layout)
        self.setWindowTitle("Find a Contact")

        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()

        if not text:
            QMessageBox.information(self, "Empty Field",
                    "Please enter a name.")
            return

        self.findText = text
        self.lineEdit.clear()
        self.hide()

    def getFindText(self):
        return self.findText


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())