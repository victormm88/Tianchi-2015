#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import numpy as np;
from sklearn.linear_model import LogisticRegression;
from sklearn.naive_bayes import GaussianNB;
import csv;
import get_result;
from sklearn.metrics import f1_score;
from sklearn.metrics import precision_score as pscore;
from sklearn.metrics import recall_score as rscore;

def main(num,date):
    data_reader=csv.reader(open('../feature_extraction/train_data_1_17.csv','rb'));
    label_reader=csv.reader(open('../feature_extraction/train_label_1_17.csv','rb'));
    test_reader=csv.reader(open('../feature_extraction/train_data_18th.csv','rb'));
    tl_reader=csv.reader(open('../feature_extraction/train_label_18th.csv','rb'));

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
    
    clf=GaussianNB();
    clf.fit(data_list,label_list);
    
    for row in test_reader:
        test_list.append(row);
    for row in tl_reader:
        tl_list+=row;

    test_list=np.array(test_list).astype(int);
    tl_list=np.array(tl_list).astype(int);
    

    csv_look=csv.writer(open('cacaca.csv','wb'));

    correct_num=0.0;
    one_num=0.0;
    Y=clf.predict(test_list);
    for i in range(len(Y)):
        if Y[i]==0:
            csv_look.writerow(test_list[i]);
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
    #get_result.get_result(Y);

if __name__=='__main__':
    main(12,17);
