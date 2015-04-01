#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

f_whole_test=open('whole_test.csv','wb');
f_buy_test=open('buy_test.csv','wb');
f_user=open('../train_data/user.csv','rb');
f_trian=open('../train_data/cv_train.csv','wb');

csv_writer=csv.writer(f_trian);
csv_reader=csv.reader(f_user);
whole_writer=csv.writer(f_whole_test);
buy_writer=csv.writer(f_buy_test);

tittle=csv_reader.next();

whole_writer.writerow(tittle);
buy_writer.writerow(tittle);
csv_writer.writerow(tittle);

for num,row in enumerate(csv_reader):
    if row[5][:10]=='2014-12-17' or row[5][:10]=='2014-12-18':
        whole_writer.writerow(row);
        if(row[2]=='4'):
            buy_writer.writerow(row);
    else:
        csv_writer.writerow(row);
    if num%1000000==0:
        print num;

f_whole_test.close();
f_buy_test.close();
f_user.close();
f_trian.close();
