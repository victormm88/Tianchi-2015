#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import numpy as np;
from sklearn.linear_model import LogisticRegression;
import csv;
import get_result;
from sklearn.metrics import f1_score;
from sklearn.metrics import precision_score as pscore;
from sklearn.metrics import recall_score as rscore;

def main(num,date):
    data_reader=csv.reader(open('../feature_extraction/test_train_data_10_17_add_uc_actbef_pair.csv','rb'));
    data_reader.next();
    label_reader=csv.reader(open('../feature_extraction/new_test_train_label_10_17.csv','rb'));
    test_reader=csv.reader(open('../result/possible_feature_2014-12-18_test_add_uc_actbef_pair.csv','rb'));
    test_reader.next();
    tl_reader=csv.reader(open('../feature_extraction/train_label_2014-12-18th_hua.csv','rb'));

    data_list=[];
    label_list=[];
    test_list=[];
    tl_list=[];

    for row in data_reader:
        data_list.append(row);
    
    for row in label_reader:
        label_list+=row;
    
    
    data_list=np.array(data_list).astype(int);
    label_list=np.array(label_list).astype(int);
    
    print data_list.shape;
    print label_list.shape;
    
    c=1;
    LR=LogisticRegression(C=c,penalty='l1');
    LR.fit(data_list,label_list);
    
    for row in test_reader:
        test_list.append(row);
    test_list=np.array(test_list).astype(int);
    Y=LR.predict(test_list);
    '''
    for row in tl_reader:
        tl_list+=row;

    tl_list=np.array(tl_list).astype(int);
    
    correct_num=0.0;
    one_num=0.0;
    #for i in range(100):
    #    print Y[i],test_list[i];
    for i in range(len(Y)):
        if Y[i]==tl_list[i]:
            correct_num+=1;
            if Y[i]==1:
                one_num+=1;
    print 'n',correct_num;
    print 'o',one_num;
    print 'r',float(correct_num)/len(Y);
    f1=f1_score(tl_list,Y,average="binary");
    p=pscore(tl_list,Y,average="binary");
    r=rscore(tl_list,Y,average="binary");
    print 'f1',f1;
    print 'p',p;
    print 'r',r;
    #T=LR.predict_proba(test_list);
    #'''
    get_result.get_result(Y);

if __name__=='__main__':
    main(12,17);
