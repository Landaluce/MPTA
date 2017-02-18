import csv
import itertools

#Uploading all Organizational Identity words into a list called new_list
empt_list = []
iter_count = 0
with open('OrgID.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter= ' ')
    for row in reader:
        empt_list.append(row)
        iter_count += 1
    org_iden = list(itertools.chain(*empt_list))
    print org_iden
    print iter_count