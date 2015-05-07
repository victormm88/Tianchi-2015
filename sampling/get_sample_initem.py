#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import MySQLdb;


def main(file_name,new_filename):
    csv_reader=csv.reader(open(file_name,'rb'));
    csv_writer=csv.writer(open(new_filename,'wb'));
    db.MySQLdb.connect('localhost','root','','Recommender');
    cursor=db.cursor();
    for row in csv_reader:
        sql="""select * from train_data where item_id="%s" """ % row[1];
        resulf_num=cursor.execute(sql);
        if resulf_num == 0:
            continue;
        sql="""select * from train_data where user_id="%s" """ % row[0];
        resulf_num=cursor.execute(sql);
        if resulf_num == 0:
            continue;
        csv_writer.writerow(row);


if __name__ == '__main__':
    main(file_name,new_filename);
