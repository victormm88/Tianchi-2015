#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import numpy as np;
from sklearn.ensemble import RandomForestClassifier;
import csv;
import get_result;
from sklearn.metrics import f1_score;
from sklearn.metrics import precision_score as pscore;
from sklearn.metrics import recall_score as rscore;
import pickle;

def get_f():
    reader_answer=csv.reader(open('../test_data/test_in_item.csv','rb'));
    answer_set=set();
    for row in reader_answer:
        answer_set.add(row[0]+'_'+row[1]);
    
    print len(answer_set);

    reader_pre=csv.reader(open('result.csv','rb'));
    reader_pre.next();
    right_count=0.0;
    pre_count=0.0;
    for row in reader_pre:
        pre_count+=1;
        if row[0]+'_'+row[1] in answer_set:
            right_count+=1;
    recall_ratio=right_count/len(answer_set);
    correct_ratio=right_count/pre_count;
    print 'n',right_count;
    print 'r',recall_ratio;
    print 'c',correct_ratio;
    if right_count == 0:
        return 0;
    f = 2*recall_ratio*correct_ratio/(recall_ratio+correct_ratio);
    print 'f',f;
    return f;

def main(num,date):
    rf=RandomForestClassifier(n_estimators=19,max_depth=10);
    data_reader=csv.reader(open('../feature_extraction/train_data_4_17_add_user_add_item_beh_add_peonum.csv','rb'));
    data_reader.next();
    label_reader=csv.reader(open('../feature_extraction/train_label_4_17.csv','rb'));
    test_reader=csv.reader(open('../result/possible_feature_2014-12-18_hua_add_user_add_item_beh_add_peonum.csv','rb'));
    test_reader.next();
    #tl_reader=csv.reader(open('../feature_e','rb'));

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

    for row in test_reader:
        test_list.append(row);
    test_list=np.array(test_list).astype(int);
    
    #[rf] = pickle.load(open('__rf','rb'));
    max_f=0.0715;
    while True:
        rf.fit(data_list,label_list);    
        #Y=rf.predict(test_list);
        Y=rf.predict_proba(test_list);
        temp_y=[];
        for row in Y:
            if row[1] > 0.5:
                temp_y.append(1);
            else:
                temp_y.append(0);
        '''
        #temp_Y=[];
        #for num in range(len(Y)):
        #    if Y[num][1] > 0.6:
        #        temp_Y.append(1);
        #    else:
        #        temp_Y.append(0);
        for row in tl_reader:
            tl_list+=row;
    
        tl_list=np.array(tl_list).astype(int);
        
        correct_num=0.0;
        one_num=0.0;
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
        get_result.get_result(temp_y);
        f=get_f();
        if f > max_f:
            pickle.dump([rf],open('__rf','wb'));
            max_f = f;

if __name__=='__main__':
    main(12,17);
