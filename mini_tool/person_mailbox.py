"""
this function is translate 'Cao, Chris L. (NSB - CN/Hangzhou) <chris.l.cao@nokia-sbell.com>; Chen, Wei 7. (NSB - CN/Hangzhou) <wei.7.chen@nokia-sbell.com>'
to below format and save to csv file
Cao, Chris L. chris.l.cao@nokia-sbell.com
Chen, Wei 7. wei.7.chen@nokia-sbell.com
usage: copy mailbox from outlook and paste to notepad (is source_file in function), then run this script
"""

import csv

def person_mailbox(source_file, destination_file):
	"""
	source_file:txt file containing raw data
	destination_file: csv file to save mailbox for each person
	"""
	with open(source_file, 'r') as file_to_read:
		person_mailbox_dic = {}
		for line in file_to_read:
			list = line.split(';')
			for item in list:
				item = item.lstrip()
				# change "Cao, Chris L. (NSB - CN/Hangzhou) <chris.l.cao@nokia-sbell.com>" to "Cao, Chris L. ; <chris.l.cao@nokia-sbell.com>"
				item = item.replace("(NSB - CN/Hangzhou)", ';')
				item_list = item.split(';')
				# item_list[1].strip()[1:-1] is to remove '<' and '>' in <ling.2.zhao@nokia-sbell.com>
				person_mailbox_dic[item_list[0].strip()] = item_list[1].strip()[1:-1]
		print(person_mailbox_dic)

	# to avoid empty row between 2 records, using newline=''
	with open(destination_file, 'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerows(person_mailbox_dic.items())


if	__name__ == '__main__':
	file = 'D:\\name_list.txt'
	person_mailbox(file, 'D:\\person_mailbox.csv')
