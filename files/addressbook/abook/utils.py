import datetime
import string
import re

from .errors import InvalidInputError

def validate_fields(contact_dict):
	validate_first_name(contact_dict['first_name'])
	validate_dob(contact_dict['dob'])
	validate_phone(contact_dict['phone_number'])
	validate_email(contact_dict['email'])

def validate_first_name(first_name):
	if first_name == '':
		raise InvalidInputError('First name can not be empty')

def validate_dob(dob):
	if dob == '':
		return
	try:
		dob = dob.split('-')
		print(dob)
		dob = datetime.datetime(int(dob[0]), int(dob[1]), int(dob[2]))
	except ValueError as e:
		raise InvalidInputError(e)

def validate_phone(phone):
	if phone == '':
		return
	for digit in phone:
		if digit in string.digits + '+- ':
			continue
		raise InvalidInputError(digit + ' is not a number')
	
def validate_email(email):
	if email == '':
		return
	else:
		if not re.match('.*@.*..*', email):
			raise InvalidInputError(email + ' is not valid')