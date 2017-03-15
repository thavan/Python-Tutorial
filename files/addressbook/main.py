#! /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from abook.abook import AddressBook

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
