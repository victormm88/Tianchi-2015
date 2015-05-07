#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

def merge(file_1,file_2):
    reader_1 = csv.reader(open(file_1,'rb'));
    reader_2 = csv.reader(open(file_2,'rb'));
    tittle=reader_1.next();
    reader_2.next();
    result_set = set();
    f1_set = set();
    for row in reader_1:
        f1_set.add(row[0]+' '+row[1]);
    for row in reader_2:
        if (row[0]+' '+row[1]) in f1_set:
            result_set.add(row[0]+' '+row[1]);

    csv_writer = csv.writer(open('test.csv','wb'));
    csv_writer.writerow(tittle);
    for row in result_set:
        csv_writer.writerow(row.split());
if __name__ == '__main__':
    merge('result1.58_2.csv','result1.59.csv');
