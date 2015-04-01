#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

csv_reader=csv.reader(open('../test_data/whole_test.csv','rb'));
tittle=csv_reader.next();

csv_writer=csv.writer(open('positive_user.csv','wb'));
csv_writer.writerow(['user_id','item_id']);

user_dir={};

for row in csv_reader:
    if row[5][:10]=='2014-12-17' and row[2]=='4':
        #csv_writer.writerow([row[0],row[1]]);
        if not user_dir.has_key(row[0]):
            user_dir[row[0]]=0;
        user_dir[row[0]]+=1;
        

for key in user_dir.keys():
    csv_writer.writerow([key,user_dir[key]]);



