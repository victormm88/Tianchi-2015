#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys;
sys.path.append("..")
from feature_extraction.feature_tool import Get_feature
import csv;


def main(date):
    csv_reader = csv.reader(open('possible_pair.csv','rb'));
    csv_writer = csv.writer(open('possible_feature_%s.csv'%date[:10],'wb'));
    
    df = Get_feature();
    
    for num,row in enumerate(csv_reader):
        feature_dir=df.get_pair_feature(row[0],row[1],date,5);
        csv_writer.writerow(feature_dir.values());
        if num % 1000==0:
            print num;

if __name__ == '__main__':
    main('2014-12-19 6');
