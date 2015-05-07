#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;


def dis_day(date,d_day):
    month=int(date[5:7]);
    day=int(date[-2:]);
    if month == 12:
        return d_day-day;
    else:
        return d_day-day+30;

def main(num,d_day):

    csv_reader=csv.reader(open('../train_data/train_user_cleaned.csv','rb'));
    
    writer_num=csv.writer(open('positive_user_%s_%s.csv'%(num,d_day),'wb'));
    writer=csv.writer(open('positive_%s_%s.csv'%(num,d_day),'wb'));
    #csv_writer.writerow(['user_id','item_id']);
    
    user_dir={};
    
    for row in csv_reader:
        day=dis_day(row[5][:10],d_day);
        if day>num-1 or day<0:
            continue;
        if row[2]=='4':
            writer.writerow([row[0],row[1],row[5][:10]]);
            if not user_dir.has_key(row[0]):
                user_dir[row[0]]=0;
            user_dir[row[0]]+=1;
            
    for key in user_dir.keys():
        writer_num.writerow([key,user_dir[key]]);

if __name__ == '__main__':
    main(12,17);
