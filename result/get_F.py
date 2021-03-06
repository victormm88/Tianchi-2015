#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import csv;

def main(date):
    reader_answer=csv.reader(open('../test_data/test_in_item.csv'%date,'rb'));
    answer_set=set();
    for row in reader_answer:
        answer_set.add(row[0]+'_'+row[1]);

    reader_pre=csv.reader(open('result.csv','rb'));
    reader_pre.next();
    right_count=0.0;
    pre_count=0.0;
    for row in reader_pre:
        pre_count+=1;
        if row[0]+'_'+row[1] in answer_set:
            right_count+=1;
    recall_ratio=right_count/len(answer_set);
    corret_ratio=right_count/pre_count;
    return 2*recall_ratio*correct_ratio/(recall_ratio+correct_ratio);


if __name__ == '__main__':
    main(18);
