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
    if not my_dir.has_key(item_id):
        my_dir[item_id]=[{},0,0,0,0];
    my_dir[item_id][behavior_type]+=1;
    my_dir[item_id][0][user_id]=True;
    if num%1000000==0:
        print num;
    #print my_dir[user_id];
    
f_user.close();

f_record=open('Item_Info_No.csv','wb');
csv_writer=csv.writer(f_record);
csv_writer.writerow(['item_id','polularity','look_through','collection','add_car','buy']);

my_list=[];

for key in my_dir.keys():
    temp_list=my_dir[key];
    temp_list[0]=len(temp_list[0]);
    my_list.append([key]+temp_list);
    del(my_dir[key]);
    #csv_writer.writerow([key]+temp_list);

my_list.sort(key=lambda x : x[1],reverse=True);

for num,row in enumerate(my_list):
    csv_writer.writerow([num+1]+row);


f_record.close();
