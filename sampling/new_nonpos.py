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


def get_nopos(pos_num,ratio,ui_set,date,num,people_num):
    csv_writer=csv.writer(open('non_positive_%s_%s.csv'%(num,date),'wb'));

    db=MySQLdb.connect("localhost",'root','','Recommender');
    cursor=db.cursor();

    csv_reader=csv.reader(open('positive_user_%s_%s.csv'%(num,date),'rb'));
    csv_reader.next();
    sigma=pos_num*ratio/3;
    my_sum=0;
    left_num=pos_num*ratio;
    for x in xrange(left_num):
        while True:
            index_id=int(Gaussian(0,(people_num/2)))+1;
            sql='''select * from User_Info_No where index_id = '%d' ''' % (index_id);
            result_num=cursor.execute(sql);
            result=cursor.fetchone();
            if result_num==0:
                continue;
            user_id=str(result[1]);
            print user_id;    

            index_id=int(Gaussian(0,sigma))+1;
            sql='''select * from Item_Info_No where index_id = '%d' ''' % (index_id);
            result_num=cursor.execute(sql);
            result=cursor.fetchone();
            if result_num==0:
                continue;
            item_id=str(result[1]);
            
            temp_str = user_id + ',' + item_id;
            if temp_str in ui_set:
                continue;
            else:
                ui_set.add(temp_str);
                csv_writer.writerow([user_id,item_id,'2014-12-%s'%date]);
                break;
    db.close();


def main(num,d_day):
    ui_set=set();
    pos_num=0;
    
    csv_reader=csv.reader(open('positive_%s_%s.csv'%(num,d_day),'rb'));
    csv_reader.next();
    for row in csv_reader:
        ui_set.add(row[0]+','+row[1]);
        pos_num+=1;
    
    get_nopos(pos_num,5,ui_set,d_day,num,9950);


if __name__ == '__main__':
    main(12,17);
