#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

csv_reader=csv.reader(open('../train_data/cv_train.csv','rb'));
csv_test_r=csv.reader(open('buy_test.csv','rb'));
csv_test_w=csv.writer(open('buy_test_v1.csv','wb'));

tittle=csv_reader.next();
csv_test_r.next();
csv_test_w.writerow(tittle);

user_dir={};

for num , row in enumerate(csv_reader):
    user_dir[row[0]]=True;

for row in csv_test_r:
    if user_dir.has_key(row[0]):
        csv_test_w.writerow(row);
