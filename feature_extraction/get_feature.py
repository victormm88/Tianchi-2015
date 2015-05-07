#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import feature_tool;
import os;

def main(num,date):
    ft=feature_tool.Get_feature();
    
    #csv_reader=csv.reader(open('../sampling/samples_%s_%s.csv'%(num,date),'rb'));
    samples_file = 'samples_5_2014-12-02.csv';
    csv_reader=csv.reader(open('../sampling/'+samples_file,'rb'));
    csv_writer = csv.writer(open('../sampling/'+samples_file+'temp','wb'));
    #csv_reader=csv.reader(open('zou_samples.csv','rb'));
    #csv_reader.next();
    writer_data=csv.writer(open('train_data_%s_%s.csv'%(num,date),'wb'));
    writer_label=csv.writer(open('train_label_%s_%s.csv'%(num,date),'wb'));
    for num,row in enumerate(csv_reader):
        temp_dir=ft.get_pair_feature(row[0],row[1],row[3],5);
        if temp_dir['pair_last_act'] != 30 or row[2]=='0':
            writer_data.writerow(temp_dir.values());
            writer_label.writerow(row[2]);
            csv_writer.writerow(row);
        if num % 1000==1:
            print num;
    #end for
    os.rename('../sampling/'+samples_file+'temp','../sampling/'+samples_file);

if __name__ == '__main__':
    main(5,17);
