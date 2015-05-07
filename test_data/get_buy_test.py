#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

def main():
    csv_reader=csv.reader(open('../train_data/item.csv','rb'));
    csv_reader.next();
    item_set=set();
    user_item_set=set();
    for row in csv_reader:
        item_set.add(row[0]);
    csv_reader=csv.reader(open('12-18th_act.csv','rb'));
    csv_writer=csv.writer(open('test_in_item.csv','wb'));
    for row in csv_reader:
        if row[2]=='4' and row[1] in item_set and row[0]+'_'+row[1] not in user_item_set:
            csv_writer.writerow([row[0],row[1]]);
            user_item_set.add(row[0]+'_'+row[1]);

if __name__ == '__main__':
    main();
