#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import MySQLdb;
import csv;

class Item:
    def __init__(self):
        self.l_look=[0,0,0];
        self.l_collection=[0,0,0];
        self.l_add=[0,0,0];
        self.l_buy=[0,0,0];
        self.l_people=[set(),set(),set()];
        self.l_pop=[set(),set(),set()];



def get_disday(time,d_month,d_day):
    month=int(time[5:7]);
    day=int(time[-2:]);
    if month==d_month:
        return d_day-day;
    else:
        return 30+d_day-day;


my_dir={};

csv_reader=csv.reader(open('../train_data/cv_train.csv','rb'));
csv_reader.next();

for num,row in enumerate(csv_reader):
    item_id=row[1];
    if not my_dir.has_key(item_id):
        my_dir[item_id]=Item();
    
    temp_item=my_dir[item_id];
    time=row[5][:10];
    dis=get_disday(time,12,17);
    behavior=int(row[2]);

    if behavior==1:
        if dis <= 3:
            temp_item.l_look[0]+=1;
            temp_item.l_pop[0].add(row[0]);
        if dis <= 7:
            temp_item.l_look[1]+=1;
            temp_item.l_pop[1].add(row[0]);
        temp_item.l_look[2]+=1;
        temp_item.l_pop[2].add(row[0]);

    elif behavior == 2:
        if dis <= 3:
            temp_item.l_collection[0]+=1;
            temp_item.l_pop[0].add(row[0]);
        if dis <= 7:
            temp_item.l_collection[1]+=1;
            temp_item.l_pop[1].add(row[0]);
        temp_item.l_collection[2]+=1;
        temp_item.l_pop[2].add(row[0]);

    elif behavior == 3:
        if dis <= 3:
            temp_item.l_add[0]+=1;
            temp_item.l_pop[0].add(row[0]);
        if dis <= 7:
            temp_item.l_add[1]+=1;
            temp_item.l_pop[1].add(row[0]);
        temp_item.l_add[2]+=1;
        temp_item.l_pop[2].add(row[0]);

    else:
        if dis <= 3:
            temp_item.l_buy[0]+=1;
            temp_item.l_pop[0].add(row[0]);
            temp_item.l_people[0].add(row[0]);
        if dis <= 7:
            temp_item.l_buy[1]+=1;
            temp_item.l_pop[1].add(row[0]);
            temp_item.l_people[1].add(row[0]);
        temp_item.l_buy[2]+=1;
        temp_item.l_pop[2].add(row[0]);
        temp_item.l_people[2].add(row[0]);

    if num % 200000 == 0:
        print num;

csv_writer = csv.writer(open('item_feature.csv','wb'));
csv_writer.writerow(['item_id','look_3','look_7','look_a','collect_3','collect_7','collect_a','add_3','add_7','add_a','buy_3','buy_7','buy_a','peo_3','peo_7','peo_a','pop_3','pop_7','pop_a']);

for key in my_dir.keys():
    temp_item=my_dir[key];
    temp_item.people[0]=len(temp_item.people[0]);
    temp_item.people[1]=len(temp_item.people[1]);
    temp_item.people[2]=len(temp_item.people[2]);
    temp_item.pop[0]=len(temp_item.pop[0]);
    temp_item.pop[1]=len(temp_item.pop[1]);
    temp_item.pop[2]=len(temp_item.pop[2]);
    csv_writer.writerow([key]+temp_item.l_look+temp_item.l_collection+temp_item.l_add+temp_item.l_buy+temp_item.people+temp_item.pop);
    
