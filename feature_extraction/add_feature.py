#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import feature_tool;

def main(samples_name,train_name,feature_name):
    sample_reader=csv.reader(open(samples_name,'rb'));
    train_reader=csv.reader(open(train_name,'rb'));
    #label_reader = csv.reader(open('test_train_label_10_17.csv','rb'));
    #label_writer = csv.writer(open('new_test_train_label_10_17.csv','wb'));
    tittle=train_reader.next();
    csv_writer=csv.writer(open(train_name[:-4]+'_add_'+feature_name+'.csv','wb'));
    
    ft=feature_tool.Get_feature();
    first_flag=False;
    feature_f=getattr(ft,'get_'+feature_name+'_feature');
    count = 0;
    for num,sample in enumerate(sample_reader):
        row = train_reader.next();
        #label = label_reader.next();
        feature_dir = feature_f(sample[0],sample[1],sample[3],5);
        if type(feature_dir) == int:
            count+=1;
            continue;
        if not first_flag:
            first_flag=True;
            csv_writer.writerow(tittle+['%s:%s' % (feature_name,len(feature_dir))]);
        csv_writer.writerow(row+feature_dir.values());
        #label_writer.writerow(label);
        if num % 1000 == 1:
            print num;
    print count;
    return;

if __name__ == '__main__':
    main('../sampling/samples_5_2014-12-02.csv','train_data_5_17_add_user_category.csv','user');
