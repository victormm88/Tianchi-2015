#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;
import MySQLdb;
import datetime;

def main():
    csv_reader =\
    csv.reader(open('train_data_5_17_add_user_category_add_user.csv','rb'));
    tittle=csv_reader.next();
    csv_writer=csv.writer(open('train_data_5_17_add_user_category_add_user_proportion.csv','wb'));
    csv_writer.writerow(tittle);
    user_tittle = ['user_last_act', 'user_look_3', 'user_look_2',
            'user_look_1', 'user_look_5', 'user_look_4', 'user_collection_4',
            'user_collection_5', 'user_collection_1', 'user_collection_2',
            'user_collection_3', 'user_last_buy', 'user_add_2', 'user_add_3',
            'user_add_1', 'user_add_4', 'user_add_5', 'user_buy_3',
            'user_buy_2', 'user_buy_1', 'user_buy_5', 'user_buy_4'];
    ui_tittle = ['pair_buy_2', 'pair_buy_3', 'pair_buy_1', 'pair_buy_4',
            'pair_buy_5', 'pair_look_4', 'pair_look_5', 'pair_look_1',
            'pair_look_2', 'pair_look_3', 'pair_add_5', 'pair_add_4',
            'pair_add_3', 'pair_add_2', 'pair_add_1', 'pair_collection_5',
            'pair_collection_4', 'pair_collection_3', 'pair_collection_2',
            'pair_collection_1', 'pair_last_buy', 'pair_last_act'];
    for row in csv_reader:
        user_feature = row[-22:];
        ui_feature = row[:22];
        user_dict = {x:int(y) for x,y in zip(user_tittle,user_feature)};
        ui_dict = {x:int(y) for x,y in zip(ui_tittle,ui_feature)};
        for key in user_dict.keys():
            if user_dict[key] == 0 or key.startswith('user_last_'):
                continue;
            temp_key = 'pair'+key[4:];
            user_dict[key] = float(ui_dict[temp_key])/user_dict[key];
        csv_writer.writerow(row[:44]+user_dict.values());
    #end for 
    return;

if  __name__ == '__main__':
    main();
