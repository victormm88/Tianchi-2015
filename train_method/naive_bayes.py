#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import numpy as np;
from sklearn.naive_bayes import GaussianNB;
import csv;
import get_result;

def main(date):
    data_reader=csv.reader(open('../feature_extraction/train_data_%s.csv'%date,'rb'));
    label_reader=csv.reader(open('../feature_extraction/train_label_%s.csv'%date,'rb'));
    test_reader=csv.reader(open('../result/possible_feature_%s.csv'%(date+1),'rb'));
    
    data_list=[];
    label_list=[];
    test_list=[];
    
    for row in data_reader:
        data_list.append(row);
    
    for row in label_reader:
        label_list+=row;
    
    
    data_list=np.array(data_list).astype(int);
    label_list=np.array(label_list).astype(int);
    
    print data_list.shape;
    print label_list.shape;
    
    clf=GaussianNB();
    clf.fit(data_list,label_list);
    
    for row in test_reader:
        test_list.append(row);
    test_list=np.array(test_list).astype(int);
    
    Y=clf.predict(test_list);
    get_result.get_result(Y);

if __name__=='__main__':
    main(17);
