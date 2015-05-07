#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

csv_reader=csv.reader(open('cacaca.csv','rb'));
row = csv_reader.next();
my_list=[];
for i in range(len(row)):
   my_list.append(dict());

for row in csv_reader:
    for i in range(len(row)):
        temp_dir=my_list[i];
        if not temp_dir.has_key(row[i]):
            temp_dir[row[i]]=0;
        temp_dir[row[i]]+=1;

#for i in range(len(my_list)):
#    my_list[i]=len(my_list[i]);

for num,ll in enumerate(my_list):
    print num,ll;
