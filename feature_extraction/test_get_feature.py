#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import feature_tool as feature_tool;

def main(num,date):
    ft=feature_tool.Get_feature();
    
    #csv_reader=csv.reader(open('../sampling/samples_%s_%s.csv'%(num,date),'rb'));
    #csv_reader=csv.reader(open('../sampling/samples_1_2014-12-17.csv','rb'));
    csv_reader=csv.reader(open('../sampling/samples_10_2014-12-17.csv','rb'));
    sample_writer=csv.writer(open('../sampling/new_samples_10_2014-12-17.csv','wb'));
    #csv_reader.next();
    writer_data=csv.writer(open('test_train_data_%s_%s.csv'%(num,date),'wb'));
    writer_label=csv.writer(open('test_train_label_%s_%s.csv'%(num,date),'wb'));
    count=0;
    for num_,row in enumerate(csv_reader):
        temp_dir=ft.get_actbefpair_feature(row[0],row[1],row[3],3,row[2]);
        if type(temp_dir) == int:
            count+=1;
            continue;
        writer_data.writerow(temp_dir.values());
        writer_label.writerow(row[2]);
        sample_writer.writerow(row);
        if num_ % 1000==1:
            print num_;
    print count;

if __name__ == '__main__':
    main(10,17);
