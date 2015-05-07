#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys
sys.path.append("..")
from feature_extraction.feature_tool import Get_feature
import csv;

csv_reader = csv.reader(open('../test_data/18th_act.csv','rb'));
csv_writer = csv.writer(open('18th_feature.csv','wb'));

df = Get_feature();

for row in csv_reader:
    feature_dir={};
    feature_dir.update(df.get_item_feature(row[1],18,30));
    feature_dir.update(df.get_pair_feature(row[0],row[1],18,30));
    feature_dir['bias']=1;
    csv_writer.writerow(feature_dir.values());

