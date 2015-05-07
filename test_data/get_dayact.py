#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

csv_reader = csv.reader(open('../train_data/user.csv','rb'));
csv_reader.next();

reader_dir={};

for row in csv_reader:
    date=row[5][:10];
    if not reader_dir.has_key(date):
        reader_dir[date]=csv.writer(open('%sth_act.csv'%(date[-5:]),'wb'));

    reader_dir[date].writerow(row);

