#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys;
import MySQLdb;
import csv;

csv_reader = csv.reader(open('pred129.csv','rb'));
csv_writer = csv.writer(open('possible_pair.csv','wb'));

db=MySQLdb.connect('localhost','root','','Recommender');
cursor=db.cursor();

for num,row in enumerate(csv_reader):
    sql="""select * from train_data where item_id="%s" """ % row[1];
    result=cursor.execute(sql);
    if result!=0:
        csv_writer.writerow(row);
    if num % 10000 ==0:
        print num;
