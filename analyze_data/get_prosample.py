#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

def main(file_name,new_filename):
    user_reader=csv.reader(open('User_Info_No.csv','rb'));
    item_reader=csv.reader(open('Item_Info_No.csv','rb'));
    
    item_reader.next();
    
    user_set=set();
    item_set=set();
    
    for row in user_reader:
        user_set.add(row[1]);
    
    for row in item_reader:
        item_set.add(row[1]);
    
    csv_reader=csv.reader(open(file_name,'rb'));
    csv_writer=csv.writer(open(new_filename,'wb'));
    
    for row in csv_reader:
        if not row[0] in user_set:
            continue;
        if not row[1] in item_set:
            continue;
        csv_writer.writerow(row);

if __name__ == '__main__':
    main('zou_samples.csv','my_samples.csv');
