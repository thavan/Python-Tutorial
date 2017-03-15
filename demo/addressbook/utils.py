import datetime

def validate_fields(contact_dict):
	error_msg = validate_first_name(contact_dict['first_name'])
	error_msg = validate_dob(contact_dict['dob'])
	error_msg = validate_phone(contact_dict['phone_number'])
	return error_msg

def validate_first_name(first_name):
	if contact_dict['first_name'].strip() == '':
		return 'First name can not be empty'

def validate_dob(dob):
	try:
		dob = dob.split('-')
		print(dob)
		dob = datetime.datetime(int(dob[0]), int(dob[1]), int(dob[2]))
	except ValueError as e:
		return str(e)

def validate_phone(phone):
	pass