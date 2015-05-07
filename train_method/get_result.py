#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

def get_result(Y):
    csv_reader=csv.reader(open('../result/possible_pair.csv','rb'));
    csv_writer=csv.writer(open('result.csv','wb'));
    csv_writer.writerow(['user_id','item_id']);
    for num,row in enumerate(csv_reader):
        if Y[num]==1:
            csv_writer.writerow([row[0],row[1]]);
        if num % 100000 ==1:
            print num;
            
