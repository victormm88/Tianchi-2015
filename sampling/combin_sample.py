#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;


def main(num,date):
    csv_writer=csv.writer(open('samples_%s_%s.csv'%(num,date),'wb'));
    
    csv_reader=csv.reader(open('positive_%s_%s.csv'%(num,date),'rb'));
    for row in csv_reader:
        csv_writer.writerow(row[0:2]+[1]+[row[2]]);
    
    csv_reader=csv.reader(open('non_positive_%s_%s.csv'%(num,date),'rb'));
    for row in csv_reader:
        csv_writer.writerow(row[0:2]+[0]+[row[2]]);

if __name__ == '__main__':
    main(12,17);
