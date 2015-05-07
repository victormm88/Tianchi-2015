#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

item_set=dict();
item_reader=csv.reader(open('../train_data/item.csv','rb'));
item_reader.next();
for row in item_reader:
    item_set[row[0]]=row[2];

csv_reader=csv.reader(open('../train_data/user.csv','rb'));
user_item_set=set();
for row in csv_reader:
    user_item_set.add(row[0]+'_'+row[1]);
csv_writer = csv.writer(open('possible_pair.csv','wb'));
for row in user_item_set:
    row=row.split('_');
    if item_set.has_key(row[1]) :
        csv_writer.writerow(row+[item_set[row[1]]]);

