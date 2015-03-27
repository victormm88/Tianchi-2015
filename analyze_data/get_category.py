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
    category_id=row[4];
    behavior_type=int(row[2]);
    if not my_dir.has_key(category_id):
        my_dir[category_id]=[set(),set(),0,0,0,0];
    my_dir[category_id][behavior_type+1]+=1;
    my_dir[category_id][0].add(user_id);
    my_dir[category_id][1].add(item_id);
    if num%1000000==0:
        print num;
    #print my_dir[user_id];
    
f_user.close();

f_record=open('Category_Info.csv','wb');
csv_writer=csv.writer(f_record);
csv_writer.writerow(['category_id','polularity','item_num','look_through','collection','add_car','buy']);

for key in my_dir.keys():
    temp_list=my_dir[key];
    temp_list[0]=len(temp_list[0]);
    temp_list[1]=len(temp_list[1]);
    csv_writer.writerow([key]+temp_list);

f_record.close();
