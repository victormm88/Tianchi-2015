#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import math;
import random;
import MySQLdb;
import csv;

def Gaussian(u,sigma):
    result=0.0;
    u1=random.random();
    u2=random.random();
    #print u1,u2;
    r=math.sqrt(-2*math.log(u1));
    theta=2*math.pi*u2;
    result=r*math.cos(theta);
    return abs(u+(result*sigma));


def get_nopos(pos_num,ratio,ui_set):
    csv_writer=csv.writer(open('non_positive.csv','wb'));
    csv_writer.writerow(['user_id','item_id']);

    db=MySQLdb.connect("localhost",'root','','Recommender');
    cursor=db.cursor();

    csv_reader=csv.reader(open('positive_user.csv','rb'));
    csv_reader.next();
    sigma=pos_num*ratio/3;
    my_sum=0;
    temp_ratio=0;
    if ratio&1==0:
        temp_ratio=ratio/2;
    else:
        temp_ratio=ratio/2+1;
    for row in csv_reader:
        my_sum+=int(row[1])*temp_ratio;
        for x in xrange(int(row[1])*temp_ratio):
            while True:
                index_id=int(Gaussian(0,sigma))+1;
                sql='''select * from Item_Info_No where index_id = '%d' ''' % (index_id);
                cursor.execute(sql);
                result=cursor.fetchone();
                temp_item=str(result[1]);
                temp_str=row[0]+','+temp_item;
                if temp_str in ui_set:
                    continue;
                else:
                    ui_set.add(temp_str);
                    csv_writer.writerow([row[0],temp_item]);
                    break;
    left_num=pos_num*ratio-my_sum;
    for x in xrange(left_num):
        while True:
            index_id=int(Gaussian(0,(left_num/3)))%9980+1;
            sql='''select * from User_Info_No where index_id = '%d' ''' % (index_id);
            cursor.execute(sql);
            result=cursor.fetchone();
            user_id=str(result[1]);
            print user_id;    

            index_id=int(Gaussian(0,sigma))+1;
            sql='''select * from Item_Info_No where index_id = '%d' ''' % (index_id);
            cursor.execute(sql);
            result=cursor.fetchone();
            item_id=str(result[1]);
            
            temp_str = user_id + ',' + item_id;
            if temp_str in ui_set:
                continue;
            else:
                ui_set.add(temp_str);
                csv_writer.writerow([user_id,item_id]);
                break;
    db.close();

ui_set=set();
pos_num=0;

csv_reader=csv.reader(open('positive.csv','rb'));
csv_reader.next();
for row in csv_reader:
    ui_set.add(row[0]+','+row[1]);
    pos_num+=1;

get_nopos(pos_num,5,ui_set);
