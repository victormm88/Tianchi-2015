#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys;
import csv;
sys.path.append("..");
import feature_extraction.feature_tool;

def main(samples_name,train_name,feature_name,d_date):
    sample_reader=csv.reader(open(samples_name,'rb'));
    train_reader=csv.reader(open(train_name,'rb'));
    tittle=train_reader.next();
    csv_writer=csv.writer(open(train_name[:-4]+'_add_'+feature_name+'.csv','wb'));
    
    ft=feature_extraction.feature_tool.Get_feature();
    first_flag=False;
    feature_f=getattr(ft,'get_'+feature_name+'_feature');
    record_dict=dict();
    for num,sample in enumerate(sample_reader):
        row = train_reader.next();
        if record_dict.has_key(sample[0]):
            csv_writer.writerow(row+record_dict[sample[0]].values());
        else:
            feature_dir = feature_f(sample[0],sample[1],d_date,5);
            if not first_flag:
                first_flag=True;
                csv_writer.writerow(tittle+['%s:%s' % (feature_name,len(feature_dir))]);
            csv_writer.writerow(row+feature_dir.values());
            record_dict[sample[0]]=feature_dir;
        if num % 1000 == 1:
            print num;
    return;

if __name__ == '__main__':
    main('possible_pair.csv','possible_feature_2014-12-19_add_user_category.csv','user','2014-12-19 0');
