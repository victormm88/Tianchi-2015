#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import test_feature_tool as feature_tool;

def main(date):
    ft=feature_tool.Get_feature();
    
    csv_reader=csv.reader(open('../test_data/12-18th_act.csv','rb'));
    writer_data=csv.writer(open('train_data_%sth_hua.csv'%date,'wb'));
    writer_label=csv.writer(open('train_label_%sth_hua.csv'%date,'wb'));
    for num,row in enumerate(csv_reader):
        temp_dir=ft.get_whole_feature(row[0],row[1],date,10);
        writer_data.writerow(temp_dir.values());
        label=0;
        if row[2]=='4':
            label=1;
        writer_label.writerow([label]);
        if num % 1000==1:
            print num;

if __name__ == '__main__':
    main('2014-12-18');
