#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

f_user=open('../train_data/cv_train.csv','rb');
csv_op=csv.reader(f_user);
tittle=csv_op.next();

my_dir={};

for num,row in enumerate(csv_op):
    user_id=row[0];
    item_id=row[1];
    behavior_type=int(row[2]);
    if not my_dir.has_key(user_id):
        my_dir[user_id]=[{},0,0,0,0];
    my_dir[user_id][behavior_type]+=1;
    my_dir[user_id][0][item_id]=True;
    if num%1000000==0:
        print num;
    #print my_dir[user_id];
    
f_user.close();

f_record=open('User_Info.csv','wb');
csv_writer=csv.writer(f_record);
csv_writer.writerow(['user_id','activeness','look_through','collection','add_car','buy']);

for key in my_dir.keys():
    temp_list=my_dir[key];
    temp_list[0]=len(temp_list[0]);
    csv_writer.writerow([key]+temp_list);

f_record.close();
